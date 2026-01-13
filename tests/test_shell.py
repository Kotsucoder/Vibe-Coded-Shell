import sys
import io
import unittest
from shell import Shell

class TestShellSingleQuotes(unittest.TestCase):
    def setUp(self):
        self.held_stdout = sys.stdout
        self.held_stdin = sys.stdin
        self.stdout = io.StringIO()
        sys.stdout = self.stdout

    def tearDown(self):
        sys.stdout = self.held_stdout
        sys.stdin = self.held_stdin

    def test_single_quotes_spaces(self):
        # command: echo 'hello    world'
        # expected: hello    world
        sys.stdin = io.StringIO("echo 'hello    world'\nexit\n")
        self.stdout = io.StringIO()
        sys.stdout = self.stdout
        
        shell = Shell()
        shell.run()
        
        output = self.stdout.getvalue()
        self.assertIn("hello    world", output)

    def test_single_quotes_empty(self):
        # command: echo 'hello''world'
        # expected: helloworld
        sys.stdin = io.StringIO("echo 'hello''world'\nexit\n")
        self.stdout = io.StringIO()
        sys.stdout = self.stdout
        
        shell = Shell()
        shell.run()
        
        output = self.stdout.getvalue()
        self.assertIn("helloworld", output)

    def test_no_quotes_collapse_spaces(self):
        # command: echo hello    world
        # expected: hello world
        sys.stdin = io.StringIO("echo hello    world\nexit\n")
        self.stdout = io.StringIO()
        sys.stdout = self.stdout
        
        shell = Shell()
        shell.run()
        
        output = self.stdout.getvalue()
        self.assertIn("hello world", output)

    def test_mixed_quotes_concatenation(self):
        # command: echo hello''world
        # expected: helloworld
        sys.stdin = io.StringIO("echo hello''world\nexit\n")
        self.stdout = io.StringIO()
        sys.stdout = self.stdout
        
        shell = Shell()
        shell.run()
        
        output = self.stdout.getvalue()
        self.assertIn("helloworld", output)

if __name__ == '__main__':
    unittest.main()
