import argparse
import sys
import os
import shlex
import re
import inspect
from typing import List, Dict, Optional, Set, Match, NoReturn

from systemrdl import RDLCompileError

from .__about__ import __version__
from .config.loader import load_cfg, AppConfig
from .plugins.exporter import get_exporter_plugins
from .plugins.importer import get_importer_plugins
from .cmd.dump import Dump
from .cmd.list_globals import ListGlobals
from .cmd.preprocess import Preprocess
from .subcommand import Subcommand


DESCRIPTION = """
PeakRDL is a control & status register model automation toolchain.

For help about a specific subcommand, try:
    peakrdl <command> --help

For more documentation, visit https://peakrdl.readthedocs.io

"""

class SubcommandHelpFormatter(argparse.RawDescriptionHelpFormatter):
    def _format_action(self, action) -> str: # type: ignore
        parts = super(argparse.RawDescriptionHelpFormatter, self)._format_action(action)
        if action.nargs == argparse.PARSER:
            parts = "\n".join(parts.split("\n")[1:])
        return parts


class ReportPluginsImpl(argparse.Action):
    CFG: AppConfig

    def __call__ (self, parser, namespace, values, option_string = None) -> NoReturn: # type: ignore
        exporters = get_exporter_plugins(self.CFG)
        importers = get_importer_plugins(self.CFG)

        print("importers:")
        for importer in importers:
            print(f"\t{importer.plugin_info}")
        print("exporters:")
        for exporter in exporters:
            print(f"\t{exporter.plugin_info}")
        sys.exit(0)


def get_file_args(path: str) -> List[str]:
    if not os.path.exists(path):
        print(f"error: file not found: {path}", file=sys.stderr)
        sys.exit(1)

    with open(path, "r", encoding='utf-8') as f:
        return shlex.split(f.read(), comments=True)


def expand_file_args(argv: List[str], _pathlist: Optional[Set[str]] = None) -> List[str]:
    if _pathlist is None:
        _pathlist = set()

    new_argv = []
    argv_iter = iter(argv)
    for arg in argv_iter:
        if arg == "-f":
            try:
                path = next(argv_iter)
            except StopIteration:
                print("error: argument -f: expected FILE", file=sys.stderr)
                sys.exit(1)

            if path in _pathlist:
                print(f"error: circular reference in -f files: '{path}' was already opened", file=sys.stderr)
                sys.exit(1)
            _pathlist.add(path)
            file_args = get_file_args(path)
            file_args = expand_file_args(file_args, _pathlist)
            _pathlist.remove(path)
            new_argv.extend(file_args)
        else:
            new_argv.append(arg)
    return new_argv


def expand_arg_vars(argv: List[str]) -> List[str]:
    """
    Expand environment variables in args
    """
    pattern = re.compile(r"\$(\w+|\{[^}]*\})")
    def repl(m: Match) -> str:
        k = m.group(1)
        if k.startswith("{") and k.endswith("}"):
            k = k[1:-1]

        v = os.environ.get(k, m.group(0))
        return v

    return [pattern.sub(repl, arg) for arg in argv]


def get_peakrdl_cfg_arg(argv: List[str]) -> Optional[str]:
    # lazy-parse argv to see if user provided a config file explicitly
    path = None
    argv_iter = iter(argv)
    for arg in argv_iter:
        if arg == "--peakrdl-cfg":
            try:
                path = next(argv_iter)
            except StopIteration:
                print("error: argument --peakrdl-cfg: expected FILE", file=sys.stderr)
                sys.exit(1)
            break
    return path


def main() -> None:
    # manually expand any -f argfiles first
    argv = expand_file_args(sys.argv[1:])
    argv = expand_arg_vars(argv)

    peakrdl_cfg_path = get_peakrdl_cfg_arg(argv)
    try:
        cfg = load_cfg(peakrdl_cfg_path)
    except ValueError as e:
        print(e.args[0], file=sys.stderr)
        sys.exit(1)

    # Collect all importers and initialize them with the config
    importers = get_importer_plugins(cfg)
    for importer in importers:
        importer._load_cfg(cfg)

    # Collect all subcommands
    subcommands: List[Subcommand] = [
        Dump(),
        ListGlobals(),
        Preprocess(),
    ]
    subcommands += get_exporter_plugins(cfg)
    for subcommand in subcommands:
        subcommand._load_cfg(cfg)

    # Check for duplicate subcommands
    sc_dict: Dict[str, Subcommand] = {}
    for sc in subcommands:
        if sc.name in sc_dict:
            other_sc = sc_dict[sc.name]
            sc_loc = f"{inspect.getfile(sc.__class__)}:{sc.__class__.__name__}"
            other_sc_loc = f"{inspect.getfile(other_sc.__class__)}:{other_sc.__class__.__name__}"
            raise RuntimeError(f"More than one exporter plugin was registered with the same name '{sc.name}': \n\t{other_sc_loc}\n\t{sc_loc}")
        sc_dict[sc.name] = sc

    # Initialize top-level arg parser
    class ReportPlugins(ReportPluginsImpl):
        CFG = cfg
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        formatter_class=SubcommandHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=__version__)
    parser.add_argument(
        "--plugins", action=ReportPlugins, nargs=0,
        help="Report the PeakRDL plugins, their versions, then exit"
    )

    # Add dummy -f and cfg flags. Not actually used as these are already
    # expanded earlier manually
    parser.add_argument(
        '-f',
        metavar="FILE",
        dest="argfile",
        help="Specify a file containing more command line arguments"
    )
    parser.add_argument(
        '--peakrdl-cfg',
        metavar="CFG",
        dest="peakrdl_cfg",
        help="Specify a PeakRDL configuration TOML file"
    )

    # Initialize subcommand arg parsers
    subgroup = parser.add_subparsers(
        title="subcommands",
        metavar="<subcommand>",
    )
    for subcommand in subcommands:
        subcommand._init_subparser(subgroup, importers)

    # Process command-line args
    options = parser.parse_args(argv)
    if not hasattr(options, 'subcommand'):
        parser.print_usage()
        print(f"{parser.prog}: error the following arguments are required: <subcommand>")
        sys.exit(1)

    # Run subcommand!
    try:
        options.subcommand.main(importers, options)
    except RDLCompileError:
        sys.exit(1)
