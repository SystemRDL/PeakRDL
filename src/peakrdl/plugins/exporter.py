from typing import List

from .entry_points import get_entry_points, get_name_from_dist
from ..subcommand import ExporterSubcommand

class ExporterSubcommandPlugin(ExporterSubcommand):
    """
    Exporters external to this package can register a subcommand implementation
    that can be loaded into PeakRDL's subcommand list.

    The subcommand definition is provided by a class extended from this class.

    .. code:: python

        class MyExporter(ExporterSubcommandPlugin):
            short_desc = "..."
            long_desc = "..."
            generates_output_file = True
            udp_definitions = []

            def add_exporter_arguments(self, arg_group: 'argparse.ArgumentParser') -> None:
                pass

            def do_export(self, top_node: 'AddrmapNode', options: 'argparse.Namespace') -> None:
                raise NotImplementedError
    """
    def __init__(self, dist_name: str, dist_version: str) -> None:
        super().__init__()
        self.dist_name = dist_name
        self.dist_version = dist_version


def get_exporter_plugins() -> List[ExporterSubcommandPlugin]:
    """
    Load any plugins that advertise themselves in their setup.py via the following:

    setup(
        ...
        entry_points = {
            "peakrdl.exporters": [
                'my_exporter_name = module.path.to:MyExporter'
            ]
        },
    )
    """
    exporters = []
    for ep, dist in get_entry_points("peakrdl.exporters"):
        cls = ep.load()
        dist_name = get_name_from_dist(dist)

        if issubclass(cls, ExporterSubcommandPlugin):
            # New-style plugin
            # Override name - always use entry point's name
            cls.name = ep.name
            exporter = cls(dist_name, dist.version)
        else:
            raise RuntimeError(f"Exporter class {cls} is expected to be extended from peakrdl.plugins.exporter.ExporterSubcommandPlugin")
        exporters.append(exporter)

    return exporters
