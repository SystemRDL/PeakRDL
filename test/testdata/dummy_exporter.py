from peakrdl.plugins.exporter import ExporterSubcommandPlugin

class DummyExporter(ExporterSubcommandPlugin):
    short_desc = "dummy command"
    generates_output_file = False
    def do_export(self, top_node, options) -> None:
        print("hello from exporter")
