import os
from unittest_utils import PeakRDLTestcase

class TestBasics(PeakRDLTestcase):
    def test_help(self):
        self.run_commandline(['-h'])

    def test_missing_subcommand(self):
        self.run_commandline([], expects_error=True)

    def test_report_plugins(self):
        self.run_commandline(['--plugins'])
        captured = self.capsys.readouterr()
        self.assertIn("systemrdl", captured.out)
        self.assertIn("uvm", captured.out)
        self.assertIn("ip-xact", captured.out)
        self.assertIn("regblock", captured.out)
        self.assertIn("html", captured.out)

    def test_parameter_override(self):
        with self.subTest("good"):
            self.run_commandline([
                'dump',
                os.path.join(self.testdata_dir, "parameters.rdl"),
                "--top", "elab_params",
                "-P", 'STR="override"',
                "-P", 'INT=2',
                "-P", "INTARR='{3,2}",
                "-P", "ONWR=woclr",
                "-P", "BOOL=false",
            ])

        with self.subTest("bad param"):
            self.run_commandline([
                'dump',
                os.path.join(self.testdata_dir, "parameters.rdl"),
                "--top", "elab_params",
                "-P", 'STR',
            ], expects_error=True)

        with self.subTest("bad syntax"):
            self.run_commandline([
                'dump',
                os.path.join(self.testdata_dir, "parameters.rdl"),
                "--top", "elab_params",
                "-P", "INTARR='{3 2}",
            ], expects_error=True)

        with self.subTest("bad type"):
            self.run_commandline([
                'dump',
                os.path.join(self.testdata_dir, "parameters.rdl"),
                "--top", "elab_params",
                "-P", 'STR=1',
            ], expects_error=True)

    def test_input_dne(self):
        self.run_commandline([
            'dump',
            os.path.join(self.testdata_dir, "this_file_doesnt_exist.rdl"),
        ], expects_error=True)
