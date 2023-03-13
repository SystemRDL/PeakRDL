import os
from unittest_utils import PeakRDLTestcase

class TestCoreCommands(PeakRDLTestcase):

    def test_dump(self):
        self.run_commandline([
            'dump',
            os.path.join(self.testdata_dir, "structural.rdl"),
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

    def test_dump_unroll(self):
        self.run_commandline([
            'dump',
            os.path.join(self.testdata_dir, "structural.rdl"),
            "--unroll",
        ])
        captured = self.capsys.readouterr()
        expected = "\n".join([
            "0x0000-0x0003: regblock.r0",
            "0x0010-0x0013: regblock.r1[0][0][0]",
            "0x0014-0x0017: regblock.r1[0][0][1]",
            "0x0018-0x001b: regblock.r1[0][0][2]",
            "0x001c-0x001f: regblock.r1[0][0][3]",
            "0x0020-0x0023: regblock.r1[0][1][0]",
            "0x0024-0x0027: regblock.r1[0][1][1]",
            "0x0028-0x002b: regblock.r1[0][1][2]",
            "0x002c-0x002f: regblock.r1[0][1][3]",
            "0x0030-0x0033: regblock.r1[0][2][0]",
            "0x0034-0x0037: regblock.r1[0][2][1]",
            "0x0038-0x003b: regblock.r1[0][2][2]",
            "0x003c-0x003f: regblock.r1[0][2][3]",
            "0x0040-0x0043: regblock.r1[1][0][0]",
            "0x0044-0x0047: regblock.r1[1][0][1]",
            "0x0048-0x004b: regblock.r1[1][0][2]",
            "0x004c-0x004f: regblock.r1[1][0][3]",
            "0x0050-0x0053: regblock.r1[1][1][0]",
            "0x0054-0x0057: regblock.r1[1][1][1]",
            "0x0058-0x005b: regblock.r1[1][1][2]",
            "0x005c-0x005f: regblock.r1[1][1][3]",
            "0x0060-0x0063: regblock.r1[1][2][0]",
            "0x0064-0x0067: regblock.r1[1][2][1]",
            "0x0068-0x006b: regblock.r1[1][2][2]",
            "0x006c-0x006f: regblock.r1[1][2][3]",
            "0x1000-0x1003: regblock.r2",
            "0x2000-0x2003: regblock.sub2[0].r1[0]",
            "0x2004-0x2007: regblock.sub2[0].r1[1]",
            "0x2008-0x200b: regblock.sub2[0].r1[2]",
            "0x200c-0x200f: regblock.sub2[0].r1[3]",
            "0x2010-0x2013: regblock.sub2[0].sub[0].r1",
            "0x2014-0x2017: regblock.sub2[0].sub[0].r2[0]",
            "0x2018-0x201b: regblock.sub2[0].sub[0].r2[1]",
            "0x201c-0x201f: regblock.sub2[0].sub[0].r3",
            "0x2020-0x2023: regblock.sub2[0].sub[1].r1",
            "0x2024-0x2027: regblock.sub2[0].sub[1].r2[0]",
            "0x2028-0x202b: regblock.sub2[0].sub[1].r2[1]",
            "0x202c-0x202f: regblock.sub2[0].sub[1].r3",
            "0x2030-0x2033: regblock.sub2[0].r2[0]",
            "0x2034-0x2037: regblock.sub2[0].r2[1]",
            "0x2038-0x203b: regblock.sub2[0].r2[2]",
            "0x203c-0x203f: regblock.sub2[0].r2[3]",
            "0x2040-0x2043: regblock.sub2[1].r1[0]",
            "0x2044-0x2047: regblock.sub2[1].r1[1]",
            "0x2048-0x204b: regblock.sub2[1].r1[2]",
            "0x204c-0x204f: regblock.sub2[1].r1[3]",
            "0x2050-0x2053: regblock.sub2[1].sub[0].r1",
            "0x2054-0x2057: regblock.sub2[1].sub[0].r2[0]",
            "0x2058-0x205b: regblock.sub2[1].sub[0].r2[1]",
            "0x205c-0x205f: regblock.sub2[1].sub[0].r3",
            "0x2060-0x2063: regblock.sub2[1].sub[1].r1",
            "0x2064-0x2067: regblock.sub2[1].sub[1].r2[0]",
            "0x2068-0x206b: regblock.sub2[1].sub[1].r2[1]",
            "0x206c-0x206f: regblock.sub2[1].sub[1].r3",
            "0x2070-0x2073: regblock.sub2[1].r2[0]",
            "0x2074-0x2077: regblock.sub2[1].r2[1]",
            "0x2078-0x207b: regblock.sub2[1].r2[2]",
            "0x207c-0x207f: regblock.sub2[1].r2[3]",
            "0x2080-0x2083: regblock.r3",
            "0x3000-0x3003: regblock.rw_reg",
            "0x3004-0x3007: regblock.rw_reg_lsb0",
            "",
        ])
        self.assertEqual(captured.out, expected)

    def test_globals(self):
        self.run_commandline([
            'globals',
            os.path.join(self.testdata_dir, "parameters.rdl"),
        ])
        captured = self.capsys.readouterr()
        expected = "\n".join([
            "myAmap",
            "amap2",
            "nested",
            "elab_params",
            "param_scope",
            "",
        ])
        self.assertEqual(captured.out, expected)

    def test_uvm(self):
        path = self.get_output_dir()
        self.run_commandline([
            'uvm',
            os.path.join(self.testdata_dir, "structural.rdl"),
            '-o', os.path.join(path, "out.sv"),
        ])

    def test_regblock(self):
        path = self.get_output_dir()
        self.run_commandline([
            'regblock',
            os.path.join(self.testdata_dir, "structural.rdl"),
            '-o', path,
        ])

    def test_ipxact(self):
        path = self.get_output_dir()
        self.run_commandline([
            'ip-xact',
            os.path.join(self.testdata_dir, "structural.rdl"),
            '-o', os.path.join(path, "out.xml"),
        ])

    def test_html(self):
        path = self.get_output_dir()
        self.run_commandline([
            'html',
            os.path.join(self.testdata_dir, "structural.rdl"),
            '-o', path,
        ])

    def test_preprocess(self):
        path = self.get_output_dir()
        self.run_commandline([
            'preprocess',
            os.path.join(self.testdata_dir, "structural.rdl"),
            '-o', os.path.join(path, "pp.sv"),
        ])
