import sys
import os
import io
import unittest

# Add parent directory to path so we can import shell
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shell import Shell

class TestShellDoubleQuotes(unittest.TestCase):
    def setUp(self):
        self.held_stdout = sys.stdout
        self.held_stdin = sys.stdin
        self.stdout = io.StringIO()
        sys.stdout = self.stdout

    def tearDown(self):
        sys.stdout = self.held_stdout
        sys.stdin = self.held_stdin

    def test_double_quotes_spaces(self):
        # command: echo "hello    world"
        # expected: hello    world
        sys.stdin = io.StringIO('echo "hello    world"\nexit\n')
        self.stdout = io.StringIO()
        sys.stdout = self.stdout
        
        shell = Shell()
        shell.run()
        
        output = self.stdout.getvalue()
        self.assertIn("hello    world", output)

    def test_double_quotes_concatenation(self):
        # command: echo "hello""world"
        # expected: helloworld
        sys.stdin = io.StringIO('echo "hello""world"\nexit\n')
        self.stdout = io.StringIO()
        sys.stdout = self.stdout
        
        shell = Shell()
        shell.run()
        
        output = self.stdout.getvalue()
        self.assertIn("helloworld", output)

    def test_mixed_quotes_1(self):
        # command: echo "shell's test"
        # expected: shell's test
        sys.stdin = io.StringIO('echo "shell\'s test"\nexit\n')
        self.stdout = io.StringIO()
        sys.stdout = self.stdout
        
        shell = Shell()
        shell.run()
        
        output = self.stdout.getvalue()
        self.assertIn("shell's test", output)

    def test_mixed_quotes_2(self):
        # command: echo 'shell "test"'
        # expected: shell "test"
        sys.stdin = io.StringIO('echo \'shell "test"\'\nexit\n')
        self.stdout = io.StringIO()
        sys.stdout = self.stdout
        
        shell = Shell()
        shell.run()
        
        output = self.stdout.getvalue()
        self.assertIn('shell "test"', output)

    def test_quoted_concatenation_mixed(self):
        # command: echo "hello"'world'
        # expected: helloworld
        sys.stdin = io.StringIO('echo "hello"\'world\'\nexit\n')
        self.stdout = io.StringIO()
        sys.stdout = self.stdout
        
        shell = Shell()
        shell.run()
        
        output = self.stdout.getvalue()
        self.assertIn("helloworld", output)

if __name__ == '__main__':
    unittest.main()
