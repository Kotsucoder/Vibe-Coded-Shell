import unittest
import sys
import os
import io

# Add parent directory to path so we can import shell
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shell import Shell

class TestSingleQuotesBackslash(unittest.TestCase):
    def setUp(self):
        self.shell = Shell()
        self.held_stdout = sys.stdout
        self.stdout = io.StringIO()
        sys.stdout = self.stdout

    def tearDown(self):
        sys.stdout = self.held_stdout

    def test_backslash_literally_in_single_quotes(self):
        # Requirement: echo 'shell\\\nscript' -> shell\\\nscript
        # We simulate the line as if typed in shell.
        # Line: echo 'shell\\\nscript'
        # Python string: "echo 'shell\\\\\\nscript'"
        line = "echo 'shell\\\\\\nscript'"
        parts = self.shell.parse_line(line)
        
        # Verify parsed arguments
        # The argument should be literally: shell\\\nscript
        self.assertEqual(parts[1], "shell\\\\\\nscript")
        
        # Verify echo output
        self.shell.builtin_echo(*parts[1:])
        output = self.stdout.getvalue().strip()
        self.assertEqual(output, "shell\\\\\\nscript")

    def test_backslash_double_quote_in_single_quotes(self):
        # Requirement: echo 'example\"test' -> example\"test
        # Line: echo 'example\"test'
        # Python string: "echo 'example\\\"test'"
        line = "echo 'example\\\"test'"
        parts = self.shell.parse_line(line)
        
        # Verify parsed arguments
        # The argument should be literally: example\"test
        self.assertEqual(parts[1], 'example\\"test')
        
        # Verify echo output
        # Clear stdout
        self.stdout.seek(0)
        self.stdout.truncate(0)
        
        self.shell.builtin_echo(*parts[1:])
        output = self.stdout.getvalue().strip()
        self.assertEqual(output, 'example\\"test')

    def test_backslash_at_end_of_single_quotes(self):
        # echo 'trailing\' -> trailing\
        line = "echo 'trailing\\'"
        parts = self.shell.parse_line(line)
        self.assertEqual(parts[1], "trailing\\")

if __name__ == '__main__':
    unittest.main()
