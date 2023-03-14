import unittest
import datetime
import os

from peakrdl.config import schema

class TestSchema(unittest.TestCase):
    def test_extract_base_types(self):
        sch = {
            "str": schema.String(),
            "int": schema.Integer(),
            "float": schema.Float(),
            "bool": schema.Boolean(),
            "datetime": schema.DateTime(),
            "date": schema.Date(),
            "time": schema.Time(),
            "int_array": [schema.Integer()],
            "user_mapping": {"*": schema.Integer()}
        }

        sch = schema.normalize(sch)

        raw_data = {
            "str": "hello",
            "int": 123,
            "float": 1.234,
            "bool": True,
            "datetime": datetime.datetime.now(),
            "date": datetime.date.today(),
            "time": datetime.time(1,2,3),
            "int_array": [10,20,30],
            "user_mapping": {
                "foo": 1,
                "bar": 2,
            }
        }

        data = sch.extract(raw_data, __file__, "testcase")

        # Expect the same
        assert data == raw_data

    def test_bad_type(self):
        with self.subTest("int"):
            sch = schema.Integer()
            raw_data = "hello"
            with self.assertRaises(schema.SchemaException):
                sch.extract(raw_data, __file__, "testcase")

        with self.subTest("array elem"):
            sch = [schema.Integer()]
            sch = schema.normalize(sch)
            raw_data = ["a", "b"]
            with self.assertRaises(schema.SchemaException):
                sch.extract(raw_data, __file__, "testcase")

        with self.subTest("array"):
            sch = [schema.Integer()]
            sch = schema.normalize(sch)
            raw_data = "hi"
            with self.assertRaises(schema.SchemaException):
                sch.extract(raw_data, __file__, "testcase")

        with self.subTest("fixed mapping"):
            sch = {"a":schema.Integer()}
            sch = schema.normalize(sch)
            raw_data = "hi"
            with self.assertRaises(schema.SchemaException):
                sch.extract(raw_data, __file__, "testcase")

        with self.subTest("user mapping"):
            sch = {"*":schema.Integer()}
            sch = schema.normalize(sch)
            raw_data = "hi"
            with self.assertRaises(schema.SchemaException):
                sch.extract(raw_data, __file__, "testcase")

    def test_paths(self):
        this_dir = os.path.dirname(__file__)

        with self.subTest("any path"):
            sch = schema.Path()
            raw_data = "run.sh"
            data = sch.extract(raw_data, __file__, "testcase")
            self.assertEqual(
                data,
                os.path.abspath(os.path.join(this_dir, "run.sh"))
            )

        with self.subTest("dir"):
            sch = schema.DirectoryPath()
            raw_data = "testdata"
            data = sch.extract(raw_data, __file__, "testcase")
            self.assertEqual(
                data,
                os.path.abspath(os.path.join(this_dir, "testdata"))
            )

        with self.subTest("file"):
            sch = schema.FilePath()
            raw_data = "run.sh"
            data = sch.extract(raw_data, __file__, "testcase")
            self.assertEqual(
                data,
                os.path.abspath(os.path.join(this_dir, "run.sh"))
            )

    def test_path_errors(self):
        with self.subTest("exists"):
            sch = schema.Path()
            raw_data = "dne"
            with self.assertRaises(schema.SchemaException):
                sch.extract(raw_data, __file__, "testcase")

        with self.subTest("isfile"):
            sch = schema.FilePath()
            raw_data = "testdata"
            with self.assertRaises(schema.SchemaException):
                sch.extract(raw_data, __file__, "testcase")

        with self.subTest("isdir"):
            sch = schema.DirectoryPath()
            raw_data = "run.sh"
            with self.assertRaises(schema.SchemaException):
                sch.extract(raw_data, __file__, "testcase")

    def test_py_errors(self):
        sch = schema.PythonObjectImport()

        with self.subTest("syntax"):
            raw_data = "bad import spec"
            with self.assertRaises(schema.SchemaException):
                sch.extract(raw_data, __file__, "testcase")

        with self.subTest("module dne"):
            raw_data = "dne_module:ClassName"
            with self.assertRaises(schema.SchemaException):
                sch.extract(raw_data, __file__, "testcase")

        with self.subTest("cLass dne"):
            raw_data = "sys:ClassDNE"
            with self.assertRaises(schema.SchemaException):
                sch.extract(raw_data, __file__, "testcase")
