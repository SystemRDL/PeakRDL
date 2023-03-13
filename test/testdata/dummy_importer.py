from peakrdl.plugins.importer import ImporterPlugin

class DummyImporter(ImporterPlugin):
    file_extensions = ["xml"]

    def is_compatible(self, path: str) -> bool:
        return False
