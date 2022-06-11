from typing import TYPE_CHECKING, List
import argparse
import os
import sys
import shlex
import re

from systemrdl import RDLCompiler
from systemrdl.messages import FileSourceRef

from .importer import Importer
from .plugins.importer import get_importer_plugins

if TYPE_CHECKING:
    from systemrdl.node import AddrmapNode


class LoadArgsFromFile (argparse.Action):
    def __call__ (self, parser, namespace, values, option_string = None):
        argfile = values

        if not os.path.exists(argfile):
            print(f"file not found: {argfile}", file=sys.stderr)
            sys.exit(1)

        with open(argfile, "r", encoding='utf-8') as f:
            parser.parse_args(
                shlex.split(f.read(), comments=True),
                namespace
            )


class Subcommand:
    """
    Base command line interface subcommand class
    """

    #: Subcommand name
    name = None

    #: Short-form description
    short_desc = None

    #: Longer-form description
    #: If left as None, inherits short_desc
    long_desc = None


    def _init_subparser(self, subgroup: 'argparse._SubParsersAction') -> None:
        assert isinstance(self.name, str)
        assert isinstance(self.short_desc, str)
        subparser = subgroup.add_parser(
            self.name,
            help=self.short_desc,
            description=(self.long_desc or self.short_desc)
        )
        self.add_arguments(subparser)
        subparser.set_defaults(subcommand=self)

        subparser.add_argument(
            '-f',
            metavar="FILENAME",
            action=LoadArgsFromFile,
            help="Specify a file containing more command line arguments"
        )


    def add_arguments(self, parser: 'argparse.ArgumentParser') -> None:
        pass


    def main(self, options: 'argparse.Namespace') -> None:
        raise NotImplementedError



class ExporterSubcommand(Subcommand):
    """
    Basic PeakRDL exporter subcommand.
    Most subcommands will fall under this category as they do the following:
    - Compile one or more RDL files
    - Optionally import other non-RDL sources
    - Elaborate the register model
    - Export <something>
    """

    #: Whether this subcommand should require the user to provide an output path
    generates_output_file = True

    def __init__(self) -> None:
        self.importers = get_importer_plugins()

    def add_arguments(self, parser: 'argparse.ArgumentParser') -> None:
        compiler_arg_group = parser.add_argument_group("compilation args")
        compiler_arg_group.add_argument(
            "input_files",
            metavar="FILE",
            nargs="+",
            help="One or more input files"
        )
        compiler_arg_group.add_argument(
            "-t", "--top",
            dest="top_def_name",
            metavar="TOP",
            default=None,
            help="Explicitly choose which addrmap  in the root namespace will be the "
                 "top-level component. If unset, The last addrmap defined will be chosen"
        )
        compiler_arg_group.add_argument(
            "--rename",
            dest="inst_name",
            default=None,
            help="Overrides the top-component's instantiated name. By default, the "
                 "instantiated name is the same as the component's type name"
        )
        compiler_arg_group.add_argument(
            "-I",
            dest="incdirs",
            metavar="INCDIR",
            action="append",
            help='Search directory for files included with `include "filename"',
        )
        compiler_arg_group.add_argument(
            "-P",
            dest="parameters",
            metavar="PARAMETER=VALUE",
            action="append",
            default=[],
            help='Specify value for a top-level SystemRDL parameter',
        )

        # TODO: Add the following:
        #   - warning/error enablement?

        for importer in self.importers:
            importer_arg_group = parser.add_argument_group(f"{importer.name} importer args")
            importer.add_importer_arguments(importer_arg_group)

        exporter_arg_group = parser.add_argument_group("exporter args")
        self.add_exporter_arguments(exporter_arg_group)


    def add_exporter_arguments(self, arg_group: 'argparse.ArgumentParser') -> None:
        if self.generates_output_file:
            arg_group.add_argument(
                "-o",
                dest="output",
                required=True,
                help="Output path",
            )


    def main(self, options: 'argparse.Namespace') -> None:
        rdlc = RDLCompiler()

        # Parse parameters
        parameters = {}
        for raw_param in options.parameters:
            m = re.fullmatch(r"(\w+)=(.+)", raw_param)
            if not m:
                rdlc.msg.fatal(f"Invalid parameter argument: {raw_param}")

            p_name = m.group(1)
            try:
                p_value = rdlc.eval(m.group(2))
            except ValueError:
                rdlc.msg.fatal(f"Unable to parse value '{m.group(2)}' for parameter '{p_name}'")
            parameters[p_name] = p_value

        # Compile/Import files
        for file in options.input_files:
            if not os.path.exists(file):
                rdlc.msg.fatal(f"Input file does not exist: {file}")

            ext = os.path.splitext(file)[1].strip(".")
            if ext == "rdl":
                # Is SystemRDL file
                rdlc.compile_file(
                    file,
                    incl_search_paths=options.incdirs,
                )
            else:
                # Is foreign input file.

                # Search which importer to use by extension first
                importer_candidates = [] # type: List[Importer]
                for importer in self.importers:
                    if ext in importer.file_extensions:
                        importer_candidates.append(importer)

                # Do 2nd pass if needed
                importer = None
                if len(importer_candidates) == 1:
                    importer = importer_candidates[0]
                elif len(importer_candidates) > 1:
                    # ambiguous which importer to use
                    # Do 2nd pass compatibility check
                    for importer_candidate in importer_candidates:
                        if importer_candidate.is_compatible(file):
                            importer = importer_candidate
                            break

                if not importer:
                    rdlc.msg.fatal(
                        "Unknown file type. Could not find any importers capable of reading this file.",
                        FileSourceRef(file)
                    )

                importer.do_import(rdlc, options, file)


        # Elaborate the design
        try:
            root = rdlc.elaborate(
                top_def_name=options.top_def_name,
                inst_name=options.inst_name,
                parameters=parameters
            )
        except (ValueError, TypeError) as e:
            # Parameter issues raise ValueError or TypeError
            # TODO: Fix exception types once they become specialized in the compiler
            rdlc.msg.fatal(e.args[0])

        # Run exporter
        self.do_export(root.top, options)


    def do_export(self, top_node: 'AddrmapNode', options: 'argparse.Namespace') -> None:
        raise NotImplementedError
