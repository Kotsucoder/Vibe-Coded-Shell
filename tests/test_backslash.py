import unittest
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
        # echo before\     after -> ["before  after"] (before + space + after, wait. The prompt says "before  after")
        # Let's check the prompt again:
        # echo before\     after | before  after | The backslash preserves the first space literally, but the shell collapses the subsequent unescaped spaces.
        # So "before" + " " + "after" -> "before after" ?? 
        # No, "before\ " -> "before "
        # Then "    " (spaces) -> separator
        # Then "after"
        # So args should be ["echo", "before ", "after"] -> output "before  after" (echo joins with space)
        # Ah, echo joins arguments with a space.
        # If args is ["echo", "before ", "after"], output is "before  after". Correct.
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
