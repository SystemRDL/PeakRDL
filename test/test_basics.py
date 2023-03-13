import os
import shutil
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

    def test_dump(self):
        self.run_commandline([
            'dump',
            os.path.join(self.examples_dir, "atxmega_spi.rdl"),
        ])
        captured = self.capsys.readouterr()
        expected = "\n".join([
            "0x0-0x0: atxmega_spi.CTRL",
            "0x1-0x1: atxmega_spi.INTCTRL",
            "0x2-0x2: atxmega_spi.STATUS",
            "0x3-0x3: atxmega_spi.DATA",
            "",
        ])
        self.assertEqual(captured.out, expected)

    def test_dump_unroll(self):
        self.run_commandline([
            'dump',
            os.path.join(self.examples_dir, "atxmega_spi.rdl"),
            "--unroll",
        ])
        captured = self.capsys.readouterr()
        expected = "\n".join([
            "0x0-0x0: atxmega_spi.CTRL",
            "0x1-0x1: atxmega_spi.INTCTRL",
            "0x2-0x2: atxmega_spi.STATUS",
            "0x3-0x3: atxmega_spi.DATA",
            "",
        ])
        self.assertEqual(captured.out, expected)

    def test_globals(self):
        self.run_commandline([
            'globals',
            os.path.join(self.examples_dir, "atxmega_spi.rdl"),
        ])
        captured = self.capsys.readouterr()
        expected = "\n".join([
            "atxmega_spi",
            "",
        ])
        self.assertEqual(captured.out, expected)

    def test_uvm(self):
        path = self.get_output_dir()
        self.run_commandline([
            'uvm',
            os.path.join(self.examples_dir, "atxmega_spi.rdl"),
            '-o', os.path.join(path, "out.sv"),
        ])

    def test_regblock(self):
        path = self.get_output_dir()
        self.run_commandline([
            'regblock',
            os.path.join(self.examples_dir, "atxmega_spi.rdl"),
            '-o', path,
        ])

    def test_ipxact(self):
        path = self.get_output_dir()
        self.run_commandline([
            'ip-xact',
            os.path.join(self.examples_dir, "atxmega_spi.rdl"),
            '-o', os.path.join(path, "out.xml"),
        ])

    def test_html(self):
        path = self.get_output_dir()
        self.run_commandline([
            'html',
            os.path.join(self.examples_dir, "atxmega_spi.rdl"),
            '-o', path,
        ])

    def test_preprocess(self):
        path = self.get_output_dir()
        self.run_commandline([
            'preprocess',
            os.path.join(self.examples_dir, "atxmega_spi.rdl"),
            '-o', os.path.join(path, "pp.sv"),
        ])
