from typing import TYPE_CHECKING

from systemrdl import RDLCompiler

from ..subcommand import Subcommand
from ..plugins.importer import get_importer_plugins

if TYPE_CHECKING:
    import argparse

class Preprocess(Subcommand):
    name = "preprocess"
    short_desc = "Preprocess SystemRDL and write the result to a file"

    def __init__(self) -> None:
        self.importers = get_importer_plugins()

    def add_arguments(self, parser: 'argparse._ActionsContainer') -> None:
        grp = parser.add_argument_group("preprocessor args")
        grp.add_argument(
            "file",
            help="SystemRDL file to preprocess"
        )
        grp.add_argument(
            "-I",
            dest="incdirs",
            metavar="INCDIR",
            action="append",
            help='Search directory for files included with `include "filename"',
        )
        grp.add_argument(
            "-o",
            dest="output",
            required=True,
            help="Output path",
        )

    def main(self, options: 'argparse.Namespace') -> None:
        rdlc = RDLCompiler()
        f_info = rdlc.preprocess_file(options.file, options.incdirs)
        with open(options.output, 'w', encoding='utf-8') as f:
            f.write(f_info.preprocessed_text)
