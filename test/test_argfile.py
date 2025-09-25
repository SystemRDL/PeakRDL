import os
from unittest_utils import PeakRDLTestcase

class TestArgfile(PeakRDLTestcase):
    def do_argfile_test(self, filename: str):
        os.environ["PEAKRDL_TOP_TEST_ENVVAR"] = "nested"
        self.run_commandline([
            '-f', os.path.join(self.testdata_dir, filename),
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

    def test_env1(self):
        self.do_argfile_test("dump_nested_env1.f")

    def test_env2(self):
        self.do_argfile_test("dump_nested_env2.f")

    def test_this_dir(self):
        self.do_argfile_test("dump_nested_this_dir.f")

    def test_err_dne(self):
        self.run_commandline([
            '-f', os.path.join(self.testdata_dir, "dne.f"),
        ], expects_error=True)

    def test_err_missing(self):
        self.run_commandline([
            '-f',
        ], expects_error=True)

    def test_err_circular(self):
        self.run_commandline([
            '-f', os.path.join(self.testdata_dir, "circular.f"),
        ], expects_error=True)
