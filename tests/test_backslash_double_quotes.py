import sys
import os
import io
import unittest

# Add parent directory to path so we can import shell
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shell import Shell

class TestShellBackslashDoubleQuotes(unittest.TestCase):
    def setUp(self):
        self.held_stdout = sys.stdout
        self.held_stdin = sys.stdin
        self.stdout = io.StringIO()
        sys.stdout = self.stdout

    def tearDown(self):
        sys.stdout = self.held_stdout
        sys.stdin = self.held_stdin

    def test_backslash_escapes_backslash(self):
        # command: echo "A \\ escapes itself"
        # expected: A \ escapes itself
        sys.stdin = io.StringIO('echo "A \\\\ escapes itself"\nexit\n')
        self.stdout = io.StringIO()
        sys.stdout = self.stdout
        
        shell = Shell()
        shell.run()
        
        output = self.stdout.getvalue()
        self.assertIn("A \\ escapes itself", output)

    def test_backslash_escapes_double_quote(self):
        # command: echo "A \" inside double quotes"
        # expected: A " inside double quotes
        sys.stdin = io.StringIO('echo "A \\" inside double quotes"\nexit\n')
        self.stdout = io.StringIO()
        sys.stdout = self.stdout
        
        shell = Shell()
        shell.run()
        
        output = self.stdout.getvalue()
        self.assertIn('A " inside double quotes', output)

    def test_backslash_literal_otherwise(self):
        # command: echo "A \c literal backslash"
        # expected: A \c literal backslash
        sys.stdin = io.StringIO('echo "A \\c literal backslash"\nexit\n')
        self.stdout = io.StringIO()
        sys.stdout = self.stdout
        
        shell = Shell()
        shell.run()
        
        output = self.stdout.getvalue()
        self.assertIn('A \\c literal backslash', output)

if __name__ == '__main__':
    unittest.main()
