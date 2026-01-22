import unittest
import os
import sys
import io

# Add parent directory to path so we can import shell
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shell import Shell

class TestRedirection(unittest.TestCase):
    def setUp(self):
        self.test_files = []

    def tearDown(self):
        for f in self.test_files:
            if os.path.exists(f):
                os.remove(f)

    def run_command(self, command_input):
        held_stdout = sys.stdout
        held_stderr = sys.stderr
        stdout = io.StringIO()
        stderr = io.StringIO()
        sys.stdout = stdout
        sys.stderr = stderr
        
        try:
            shell = Shell()
            # We need to simulate stdin
            sys.stdin = io.StringIO(command_input + "\nexit\n")
            shell.run()
        except SystemExit:
            pass
        finally:
            sys.stdout = held_stdout
            sys.stderr = held_stderr
            sys.stdin = sys.__stdin__ # Restore stdin
        
        return stdout.getvalue(), stderr.getvalue()

    def test_redirect_stdout(self):
        filename = "test_output_1.txt"
        self.test_files.append(filename)
        
        self.run_command(f"echo hello > {filename}")
        
        self.assertTrue(os.path.exists(filename))
        with open(filename, 'r') as f:
            content = f.read().strip()
        self.assertEqual(content, "hello")

    def test_redirect_append(self):
        filename = "test_output_2.txt"
        self.test_files.append(filename)
        
        # Create file
        with open(filename, 'w') as f:
            f.write("first\n")
            
        self.run_command(f"echo second >> {filename}")
        
        with open(filename, 'r') as f:
            content = f.read().strip()
        self.assertEqual(content, "first\nsecond")

    def test_redirect_append_create(self):
        filename = "test_output_3.txt"
        self.test_files.append(filename)
        
        self.run_command(f"echo created >> {filename}")
        
        self.assertTrue(os.path.exists(filename))
        with open(filename, 'r') as f:
            content = f.read().strip()
        self.assertEqual(content, "created")

if __name__ == '__main__':
    unittest.main()
