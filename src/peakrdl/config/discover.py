from typing import Optional
import os

def discover_cfg_file() -> Optional[str]:
    """
    Discover a PeakRDL TOML config file
    """

    # 1. In current directory
    path = os.path.abspath("peakrdl.toml")
    if os.path.isfile(path):
        return path

    path = os.path.abspath(".peakrdl.toml")
    if os.path.isfile(path):
        return path

    # 2. Via environment variable
    if "PEAKRDL_CFG" in os.environ:
        path = os.environ["PEAKRDL_CFG"]
        if os.path.isfile(path):
            return path

    # 3. In home directory
    path = os.path.expanduser("~/.peakrdl.toml")
    if os.path.isfile(path):
        return path

    path = os.path.expanduser("~/.config/peakrdl.toml")
    if os.path.isfile(path):
        return path

    # 4. In /etc/
    path = "/etc/peakrdl.toml"
    if os.path.isfile(path):
        return path

    return None
