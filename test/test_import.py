import os

from unittest_utils import PeakRDLTestcase

class TestImporters(PeakRDLTestcase):
    def test_importer(self):
        self.run_commandline([
            'dump',
            os.path.join(self.testdata_dir, "structural.xml"),
            "--top", "regblock__regblock_mmap__regblock",
            "--rename", "regblock",
        ])
        captured = self.capsys.readouterr()
        expected = "\n".join([
            "0x0000-0x0003: regblock.r0",
            "0x0010-0x006f: regblock.r1[2][3][4]",
            "0x1000-0x1003: regblock.r2",
            "0x2000-0x200f: regblock.sub2[2].r1[4]",
            "0x2010-0x2013: regblock.sub2[2].sub[2].r1",
            "0x2014-0x201b: regblock.sub2[2].sub[2].r2[2]",
            "0x201c-0x201f: regblock.sub2[2].sub[2].r3",
            "0x2030-0x203f: regblock.sub2[2].r2[4]",
            "0x2080-0x2083: regblock.r3",
            "0x3000-0x3003: regblock.rw_reg",
            "0x3004-0x3007: regblock.rw_reg_lsb0",
            "",
        ])
        self.assertEqual(captured.out, expected)

    def test_bad_type(self):
        self.run_commandline([
            'dump',
            os.path.join(self.testdata_dir, "circular.f"),
        ], expects_error=True)

    def test_alt_xml_conflict(self):
        self.run_commandline([
            "--peakrdl-cfg", os.path.join(self.testdata_dir, "peakrdl.toml"),
            'dump',
            os.path.join(self.testdata_dir, "structural.xml"),
            "--top", "regblock__regblock_mmap__regblock",
            "--rename", "regblock",
        ])
