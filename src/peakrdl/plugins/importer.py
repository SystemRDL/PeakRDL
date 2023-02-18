from typing import List

from .entry_points import get_entry_points, get_name_from_dist
from ..importer import Importer

class ImporterPlugin(Importer):
    """
    Importers external to this package can register an implementation that can
    be loaded into PeakRDL

    The importer definition is provided by a class extended from this class.

    .. code:: python

        class MyImporter(ImporterPlugin):
            file_extensions = ["foo"]

            def is_compatible(self, path: str) -> bool:
                raise NotImplementedError

            def add_importer_arguments(self, arg_group: 'argparse.ArgumentParser') -> None:
                pass

            def do_import(self, rdlc: 'RDLCompiler', options: 'argparse.Namespace', path: str):
                raise NotImplementedError
    """
    def __init__(self, dist_name: str, dist_version: str) -> None:
        super().__init__()
        self.dist_name = dist_name
        self.dist_version = dist_version


def get_importer_plugins() -> List[ImporterPlugin]:
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
        cls = ep.load()
        dist_name = get_name_from_dist(dist)

        if issubclass(cls, ImporterPlugin):
            # New-style plugin
            # Override name - always use entry point's name
            cls.name = ep.name
            importer = cls(dist_name, dist.version)
        else:
            raise RuntimeError(f"Importer class {cls} is expected to be extended from peakrdl.plugins.importer.ImporterPlugin")
        importers.append(importer)

    return importers
