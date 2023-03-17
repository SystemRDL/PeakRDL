import os
from unittest_utils import PeakRDLTestcase

class TestBasics(PeakRDLTestcase):

    def test_cfg_file_errors(self):
        with self.subTest("file DNE"):
            self.run_commandline([
                '--peakrdl-cfg', os.path.join(self.testdata_dir, "dne.toml"),
                "--plugins"
            ], expects_error=True)

        with self.subTest("file missing"):
            self.run_commandline([
                "--plugins",
                '--peakrdl-cfg',
            ], expects_error=True)

        with self.subTest("file invalid"):
            self.run_commandline([
                '--peakrdl-cfg', os.path.join(self.testdata_dir, "circular.f"),
                "--plugins"
            ], expects_error=True)

    def test_load_cfg_methods(self):
        with self.subTest("commandline"):
            self.run_commandline([
                "--peakrdl-cfg", os.path.join(self.testdata_dir, "peakrdl.toml"),
                '--plugins',
            ])
            captured = self.capsys.readouterr()
            self.assertIn("dummy_xml", captured.out)

        with self.subTest("cwd1"):
            cwd = os.getcwd()
            os.chdir(os.path.join(self.testdata_dir, "toml_dir1"))
            self.run_commandline([
                '--plugins',
            ])
            os.chdir(cwd)
            captured = self.capsys.readouterr()
            self.assertIn("dummy_xml1", captured.out)

        with self.subTest("cwd2"):
            cwd = os.getcwd()
            os.chdir(os.path.join(self.testdata_dir, "toml_dir2"))
            self.run_commandline([
                '--plugins',
            ])
            os.chdir(cwd)
            captured = self.capsys.readouterr()
            self.assertIn("dummy_xml2", captured.out)
            self.assertIn("dummy_xport", captured.out)

        with self.subTest("env"):
            os.environ["PEAKRDL_CFG"] = os.path.join(self.testdata_dir, "peakrdl.toml")
            self.run_commandline([
                '--plugins',
            ])
            del os.environ["PEAKRDL_CFG"]
            captured = self.capsys.readouterr()
            self.assertIn("dummy_xml", captured.out)

    def test_cfg_schema_errors(self):
        with self.subTest("bad pythonpath"):
            self.run_commandline([
                '--peakrdl-cfg', os.path.join(self.testdata_dir, "bad_pythonpath.toml"),
                "--plugins"
            ], expects_error=True)

        with self.subTest("bad namespace schema"):
            self.run_commandline([
                '--peakrdl-cfg', os.path.join(self.testdata_dir, "bad_plugin.toml"),
                "--plugins"
            ], expects_error=True)
