from typing import TYPE_CHECKING, Any, List
from importlib import metadata

from ..subcommand import ExporterSubcommand

if TYPE_CHECKING:
    from systemrdl.node import AddrmapNode
    import argparse


class ExporterSubcommandPluginWrapper(ExporterSubcommand):
    """
    Exporters external to this package can register a subcommand implementation
    that can be loaded into PeakRDL's subcommand list.

    The subcommand definition is provided by a class that mimics the
    members/methods of ExporterSubcommand without actually extending it

    .. code:: python

        class MyExporter:
            short_desc = "..."
            long_desc = "..."
            generates_output_file = True

            def add_exporter_arguments(self, arg_group: 'argparse.ArgumentParser') -> None:
                pass

            def do_export(self, top_node: 'AddrmapNode', options: 'argparse.Namespace') -> None:
                raise NotImplementedError
    """

    def __init__(self, name: str, exporter_plugin_cls: Any) -> None:
        super().__init__()

        self.plugin = exporter_plugin_cls()
        self.name = name
        self.short_desc = getattr(self.plugin, "short_desc")
        self.long_desc = getattr(self.plugin, "long_desc", None)
        self.generates_output_file = getattr(self.plugin, "generates_output_file", True)


    def __repr__(self) -> str:
        return "<%s '%s' from %s at 0x%x>" % (
            self.__class__.__qualname__,
            self.name,
            self.plugin.__class__,
            id(self)
        )


    def add_exporter_arguments(self, arg_group: 'argparse._ActionsContainer') -> None:
        super().add_exporter_arguments(arg_group)

        func = getattr(self.plugin, "add_exporter_arguments", None)
        if callable(func):
            func(arg_group)


    def do_export(self, top_node: 'AddrmapNode', options: 'argparse.Namespace') -> None:
        func = getattr(self.plugin, "do_export", None)
        if callable(func):
            func(top_node, options)
        else:
            raise NotImplementedError



def get_exporter_plugins() -> List[ExporterSubcommandPluginWrapper]:
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
    eps = metadata.entry_points().select(group='peakrdl.exporters')

    exporters = []
    for ep in eps:
        exporter = ExporterSubcommandPluginWrapper(ep.name, ep.load())
        exporters.append(exporter)

    return exporters
