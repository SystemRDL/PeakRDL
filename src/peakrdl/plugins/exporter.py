from typing import List, TYPE_CHECKING, Optional
import inspect

from .entry_points import get_entry_points, get_name_from_dist
from ..subcommand import ExporterSubcommand

if TYPE_CHECKING:
    from ..config.loader import AppConfig

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
    def __init__(self, dist_name: Optional[str]=None, dist_version: Optional[str]=None) -> None:
        super().__init__()
        self.dist_name = dist_name
        self.dist_version = dist_version

    @property
    def plugin_info(self) -> str:
        if self.dist_name and self.dist_version:
            return f"{self.name} --> {self.dist_name} {self.dist_version}"
        else:
            return f"{self.name} --> {inspect.getabsfile(type(self))}:{type(self).__name__}"


def get_exporter_plugins(cfg: 'AppConfig') -> List[ExporterSubcommandPlugin]:
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

    # Get exporter plugins from entry-points
    for ep, dist in get_entry_points("peakrdl.exporters"):
        cls = ep.load()
        dist_name = get_name_from_dist(dist)

        if issubclass(cls, ExporterSubcommandPlugin):
            # Override name - always use entry point's name
            cls.name = ep.name
            exporter = cls(dist_name=dist_name, dist_version=dist.version)
        else:
            raise RuntimeError(f"Exporter class {cls} is expected to be extended from peakrdl.plugins.exporter.ExporterSubcommandPlugin")
        exporters.append(exporter)

    # Get any additional exporter plugins from config
    for name, cls in cfg.peakrdl_cfg['plugins']['exporters'].items():
        if issubclass(cls, ExporterSubcommandPlugin):
            # Override name - always use entry point's name
            cls.name = name
            exporter = cls()
        else:
            raise RuntimeError(f"Exporter class {cls} is expected to be extended from peakrdl.plugins.exporter.ExporterSubcommandPlugin")
        exporters.append(exporter)

    return exporters
