from typing import TYPE_CHECKING, Optional
import argparse
import os
import sys
import shlex

from systemrdl import RDLCompiler

from .plugins.importer import get_importer_plugins

from . import process_input

if TYPE_CHECKING:
    from systemrdl.node import AddrmapNode


class LoadArgsFromFile (argparse.Action):
    def __call__ (self, parser, namespace, values, option_string = None): # type: ignore
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
    name = None # type: str

    #: Short-form description
    short_desc = None # type: str

    #: Longer-form description
    #: If left as None, inherits short_desc
    long_desc = None # type: Optional[str]


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


    def add_arguments(self, parser: 'argparse._ActionsContainer') -> None:
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

    def add_arguments(self, parser: 'argparse._ActionsContainer') -> None:
        compiler_arg_group = parser.add_argument_group("compilation args")
        process_input.add_rdl_compile_arguments(compiler_arg_group)
        process_input.add_elaborate_arguments(compiler_arg_group)

        process_input.add_importer_arguments(parser, self.importers)

        exporter_arg_group = parser.add_argument_group("exporter args")
        self.add_exporter_arguments(exporter_arg_group)


    def add_exporter_arguments(self, arg_group: 'argparse._ActionsContainer') -> None:
        if self.generates_output_file:
            arg_group.add_argument(
                "-o",
                dest="output",
                required=True,
                help="Output path",
            )


    def main(self, options: 'argparse.Namespace') -> None:
        rdlc = RDLCompiler()

        parameters = process_input.parse_parameters(rdlc, options.parameters)

        process_input.process_input(rdlc, self.importers, options.input_files, options)

        top = process_input.elaborate(rdlc, parameters, options)

        # Run exporter
        self.do_export(top, options)


    def do_export(self, top_node: 'AddrmapNode', options: 'argparse.Namespace') -> None:
        raise NotImplementedError
