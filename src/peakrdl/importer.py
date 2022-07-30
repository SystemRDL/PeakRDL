from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import List
    import argparse
    from systemrdl import RDLCompiler

class Importer:
    #: Importer name

    name = None # type: str

    #: List of possible file extensions.
    #: This is used as the first pass to determine if the input file shall use
    #: this importer
    file_extensions = [] # type: List[str]

    def is_compatible(self, path: str) -> bool:
        """
        If the file extension was not enough to determine which importer to use,
        this function is called and shall determine if the file is compatible
        with this importer to a high degree of confidence.

        Note: this should not attempt to validate the file's correctness, just
        perform a low-cost assessment if the file appears to match the format
        that this importer supports.
        """
        raise NotImplementedError


    def add_importer_arguments(self, arg_group: 'argparse._ActionsContainer') -> None:
        pass


    def do_import(self, rdlc: 'RDLCompiler', options: 'argparse.Namespace', path: str) -> None:
        raise NotImplementedError
