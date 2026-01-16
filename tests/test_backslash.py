import unittest
import sys
import os

# Add parent directory to path so we can import shell
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shell import Shell

class TestBackslash(unittest.TestCase):
    def setUp(self):
        self.shell = Shell()

    def test_backslash_escapes_space(self):
        # echo three\ \ \ spaces -> ["three   spaces"]
        line = "echo three\\ \\ \\ spaces"
        args = self.shell.parse_line(line)
        self.assertEqual(args, ["echo", "three   spaces"])

    def test_backslash_preserves_first_space_literal(self):
        # echo before\     after -> ["echo", "before ", "after"]
        line = "echo before\\     after"
        args = self.shell.parse_line(line)
        self.assertEqual(args, ["echo", "before ", "after"])

    def test_backslash_escapes_n(self):
        # echo test\nexample -> ["testnexample"]
        line = "echo test\\nexample"
        args = self.shell.parse_line(line)
        self.assertEqual(args, ["echo", "testnexample"])

    def test_backslash_escapes_backslash(self):
        # echo hello\\world -> ["hello\world"]
        line = "echo hello\\\\world"
        args = self.shell.parse_line(line)
        self.assertEqual(args, ["echo", "hello\\world"])

    def test_backslash_escapes_single_quote(self):
        # echo \'hello\' -> ["'hello'"]
        line = "echo \\'hello\\'"
        args = self.shell.parse_line(line)
        self.assertEqual(args, ["echo", "'hello'"])
        
    def test_backslash_escapes_double_quote(self):
         # echo \"hello\" -> ['"hello"']
        line = "echo \\\"hello\\\""
        args = self.shell.parse_line(line)
        self.assertEqual(args, ["echo", '"hello"'])

if __name__ == '__main__':
    unittest.main()
