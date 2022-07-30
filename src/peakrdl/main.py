import argparse
import sys
from typing import TYPE_CHECKING, List, Dict

from systemrdl import RDLCompileError

from .__about__ import __version__
from .plugins.exporter import get_exporter_plugins
from .cmd.dump import Dump
from .cmd.list_globals import ListGlobals


if TYPE_CHECKING:
    from .subcommand import Subcommand


DESCRIPTION = """
PeakRDL is a control & status register model automation toolchain.

For help about a specific subcommand, try:
    peakrdl <command> --help

For more documentation, visit https://peakrdl.readthedocs.io

"""


class SubcommandHelpFormatter(argparse.RawDescriptionHelpFormatter):
    def _format_action(self, action): # type: ignore
        parts = super(argparse.RawDescriptionHelpFormatter, self)._format_action(action)
        if action.nargs == argparse.PARSER:
            parts = "\n".join(parts.split("\n")[1:])
        return parts


def main() -> None:
    # Collect all subcommands
    subcommands = [
        Dump(),
        ListGlobals(),
    ] # type: List[Subcommand]
    subcommands += get_exporter_plugins()

    # Check for duplicates
    sc_dict = {} # type: Dict[str, Subcommand]
    for sc in subcommands:
        if sc.name in sc_dict:
            raise RuntimeError(f"More than one exporter plugin was registered with the same name '{sc.name}': \n\t{sc_dict[sc.name]}\n\t{sc}")
        sc_dict[sc.name] = sc

    # Initialize top-level arg parser
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        formatter_class=SubcommandHelpFormatter,
    )
    parser.add_argument("--version", action="version", version=__version__)

    # Initialize subcommand arg parsers
    subgroup = parser.add_subparsers(
        title="subcommands",
        metavar="<subcommand>",
        required=True
    )
    for subcommand in subcommands:
        subcommand._init_subparser(subgroup)

    # Execute!
    options = parser.parse_args()
    try:
        options.subcommand.main(options)
    except RDLCompileError:
        sys.exit(1)
