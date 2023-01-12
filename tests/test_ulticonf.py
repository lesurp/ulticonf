from ulticonf import Ulticonf
import unittest
import io
import os

file_content = """
foo = 1
baz = "miaou"
# bar
"""

# TODO: not sure whether this is a proper way to set env. var for a unittest
# (executed in parallel / in same process?)
os.environ["GRAOU_BAZ"] = "OUAF"
os.environ["GRAOU_FOO"] = "u"


class TestLoadCli(unittest.TestCase):
    def setUp(self):
        self.file = io.StringIO(file_content)

    def test_cli(self):
        u = Ulticonf()
        u.add_argument("--foo", type=int)
        u.add_argument("--baz", type=str)
        out = u.parse_args(["--foo", "2"])
        self.assertEqual(out.foo, 2)
        self.assertEqual(out.baz, None)

    def test_cli_file(self):
        u = Ulticonf(configuration_file=self.file)
        u.add_argument("--bar", type=int)
        u.add_argument("--foo", type=int)
        out = u.parse_args(["--bar", "2"])
        self.assertEqual(out.bar, 2)
        self.assertEqual(out.foo, 1)
        # TODO expected, but maybe not desired
        # self.assertEqual(out.baz, "miaou")

    def test_cli_file_wrong_type(self):
        u = Ulticonf(configuration_file=self.file)
        u.add_argument("--baz", type=int)
        self.assertRaises(ValueError, u.parse_args, [])

    def test_cli_env(self):
        u = Ulticonf(environment_prefix="GRAOU_")
        u.add_argument("--baz", type=str)
        u.add_argument("--foo", type=int)
        out = u.parse_args(["--foo", "2"])
        self.assertEqual(out.baz, "OUAF")
        self.assertEqual(out.foo, 2)

    def test_cli_env_wrong_type(self):
        u = Ulticonf(environment_prefix="GRAOU_")
        u.add_argument("--foo", type=int)
        self.assertRaises(ValueError, u.parse_args, [])


if __name__ == "__main__":
    unittest.main()
