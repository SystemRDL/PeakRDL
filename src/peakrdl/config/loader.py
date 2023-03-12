from typing import Optional, List, Any, Dict
import os
import sys

from . import schema

if sys.version_info[0:2] < (3, 11):
    # Prior to py3.11, tomllib is a 3rd party package
    import tomli as tomllib
else:
    # py3.11 and onwards, tomli was absorbed into the standard library as tomllib
    import tomllib

class AppConfig:
    def __init__(self, path: str, raw_data: Dict[str, Any]) -> None:
        self.path = path
        self.raw_data = raw_data

        sch = schema.normalize({
            "plugins": {
                "importers": {"*": schema.PythonObjectImport()},
                "exporters": {"*": schema.PythonObjectImport()},
            },
        })
        self.peakrdl_cfg = self.get_namepsace("peakrdl", sch)

    def get_namepsace(self, name: str, sch: schema.Schema) -> Dict[str, Any]:
        data = self.raw_data.get(name, {})
        try:
            cfg = sch.extract(data, self.path, name)
        except schema.SchemaException as e:
            print(f"{self.path}: error: {str(e)}")
            sys.exit(1)
        return cfg


def _discover_cfg_file() -> Optional[str]:
    """
    Discover a PeakRDL TOML config file
    """

    # 1. In current directory
    path = os.path.abspath("peakrdl.toml")
    if os.path.isfile(path):
        return path

    # 2.
    path = os.path.abspath(".peakrdl.toml")
    if os.path.isfile(path):
        return path

    # 3. Via environment variable
    if "PEAKRDL_CFG" in os.environ:
        path = os.environ["PEAKRDL_CFG"]
        if os.path.isfile(path):
            return path

    # 4. In home directory
    path = os.path.expanduser("~/.peakrdl.toml")
    if os.path.isfile(path):
        return path

    # 5.
    path = os.path.expanduser("~/.config/peakrdl.toml")
    if os.path.isfile(path):
        return path

    # 6. In /etc/
    path = "/etc/peakrdl.toml"
    if os.path.isfile(path):
        return path

    return None


BOOTSTRAP_SCHEMA = schema.normalize({
    "peakrdl": {
        "python_search_paths": [schema.DirectoryPath(shall_exist=False)]
    }
})

def load_cfg(argv: List[str]) -> AppConfig:
    # lazy-parse argv to see if user provided a config file explicitly
    path = None
    argv_iter = iter(argv)
    for arg in argv_iter:
        if arg == "--peakrdl-cfg":
            try:
                path = next(argv_iter)
            except StopIteration:
                print("error: argument --peakrdl-cfg: expected FILE", file=sys.stderr)
                sys.exit(1)
            break

    if path is None:
        # No config file path was provided from the command-line
        # try to discover it elsewhere
        path = _discover_cfg_file()

    if path is None:
        # Nope. Still no config file. Provide empty data
        raw_data = {}
    else:
        if not os.path.isfile(path):
            print(f"error: invalid config file path: {path}", file=sys.stderr)
            sys.exit(1)

        with open(path, 'r', encoding='utf-8') as f:
            s = f.read()
        try:
            raw_data = tomllib.loads(s)
        except tomllib.TOMLDecodeError as e:
            print(f"{path}: error: {str(e)}", file=sys.stderr)
            sys.exit(1)

    # Do a first-pass extraction to fetch additional entries to be added to PYTHONPATH
    try:
        tmp = BOOTSTRAP_SCHEMA.extract(raw_data, path, "")
    except schema.SchemaException as e:
        print(f"{path}: error: {str(e)}")
        sys.exit(1)
    for spath in tmp['peakrdl']['python_search_paths']:
        sys.path.append(spath)

    return AppConfig(path, raw_data)
