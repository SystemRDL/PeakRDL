import unittest
from unittest.mock import patch
import os

import pytest

class PeakRDLTestcase(unittest.TestCase):
    this_dir = os.path.dirname(__file__)
    testdata_dir = os.path.join(this_dir, "testdata")

    def run_commandline(self, argv, expects_error=False) -> None:
        argv = ["peakrdl"] + argv
        with patch("sys.argv", argv):
            try:
                from peakrdl.main import main
                main()
            except SystemExit as exit:
                # Program called sys.exit()
                if expects_error:
                    self.assertNotEqual(exit.code, 0)
                else:
                    self.assertEqual(exit.code, 0)
            else:
                # Program exited without a call to sys.exit()
                if expects_error:
                    self.fail("Expected SystemExit with an error exit code")

    @pytest.fixture(autouse=True)
    def capsys(self, capsys):
        self.capsys = capsys

    @pytest.fixture(autouse=True)
    def _load_request(self, request):
        self.request = request

    def get_output_dir(self):
        path = os.path.join(self.this_dir, "test.out", type(self).__name__, self.request.node.name)
        os.makedirs(path, exist_ok=True)
        return path
