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

    def test_f_argfile(self):
        self.run_commandline([
            '-f', os.path.join(self.testdata_dir, "dump_nested.f"),
        ])
        captured = self.capsys.readouterr()
        expected = "\n".join([
            "0x00-0x03: nested.rf_inst.r_inst1",
            "0x04-0x07: nested.rf_inst.r_inst2",
            "0x08-0x0b: nested.r1_inst",
            "0x0c-0x0f: nested.r1_inst2",
            "",
        ])
        self.assertEqual(captured.out, expected)

    def test_f_argfile_errors(self):
        with self.subTest("file DNE"):
            self.run_commandline([
                '-f', os.path.join(self.testdata_dir, "dne.f"),
            ], expects_error=True)

        with self.subTest("file missing"):
            self.run_commandline([
                '-f',
            ], expects_error=True)

        with self.subTest("circular ref"):
            self.run_commandline([
                '-f', os.path.join(self.testdata_dir, "circular.f"),
            ], expects_error=True)
