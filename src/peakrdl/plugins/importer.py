from typing import TYPE_CHECKING, Any, List

from .entry_points import get_entry_points, get_name_from_dist
from ..importer import Importer

if TYPE_CHECKING:
    import argparse
    from systemrdl import RDLCompiler

class ImporterPluginWrapper(Importer):
    """
    Importers external to this package can register an implementation that can
    be loaded into PeakRDL

    The importer definition is provided by a class that mimics the
    members/methods of the Importer class without actually extending it

    .. code:: python

        class MyImporter:
            file_extensions = ["foo"]

            def is_compatible(self, path: str) -> bool:
                raise NotImplementedError

            def add_importer_arguments(self, arg_group: 'argparse.ArgumentParser') -> None:
                pass

            def do_import(self, rdlc: 'RDLCompiler', options: 'argparse.Namespace', path: str):
                raise NotImplementedError
    """

    def __init__(self, name: str, importer_plugin_cls: Any, dist_name: str, dist_version: str) -> None:
        self.plugin = importer_plugin_cls()
        self.name = name
        self.dist_name = dist_name
        self.dist_version = dist_version
        self.file_extensions = getattr(self.plugin, "file_extensions", [])

    def __repr__(self) -> str:
        return "<%s '%s' from %s at 0x%x>" % (
            self.__class__.__qualname__,
            self.name,
            self.plugin.__class__,
            id(self)
        )

    def is_compatible(self, path: str) -> bool:
        func = getattr(self.plugin, "is_compatible", None)
        if callable(func):
            return func(path)
        else:
            raise NotImplementedError


    def add_importer_arguments(self, arg_group: 'argparse._ActionsContainer') -> None:
        func = getattr(self.plugin, "add_importer_arguments", None)
        if callable(func):
            func(arg_group)


    def do_import(self, rdlc: 'RDLCompiler', options: 'argparse.Namespace', path: str) -> None:
        func = getattr(self.plugin, "do_import", None)
        if callable(func):
            func(rdlc, options, path)
        else:
            raise NotImplementedError



def get_importer_plugins() -> List[ImporterPluginWrapper]:
    """
    Load any plugins that advertise themselves in their setup.py via the following:

    setup(
        ...
        entry_points = {
            "peakrdl.importers": [
                'my_importer_name = module.path.to:MyImporter'
            ]
        },
    )
    """
    importers = []
    for ep, dist in get_entry_points("peakrdl.importers"):
        importer = ImporterPluginWrapper(
            ep.name, ep.load(),
            get_name_from_dist(dist), dist.version
        )
        importers.append(importer)

    return importers
