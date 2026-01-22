import os
import sys
import subprocess
import time

def run_test(command_input, check_file, expected_content):
    print(f"Testing: {command_input.strip()} -> {check_file}")
    
    # Run shell as subprocess
    process = subprocess.Popen(
        [sys.executable, "shell.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate(input=command_input + "\nexit\n")
    
    if os.path.exists(check_file):
        with open(check_file, 'r') as f:
            content = f.read().strip()
        
        if content == expected_content:
            print("PASS")
            os.remove(check_file)
            return True
        else:
            print(f"FAIL: File content mismatch.")
            print(f"Expected: '{expected_content}'")
            print(f"Got: '{content}'")
            os.remove(check_file)
            return False
    else:
        print(f"FAIL: File {check_file} not created.")
        return False

# Test 1: Echo to file
if not run_test("echo hello > output1.txt", "output1.txt", "hello"):
    sys.exit(1)

# Test 2: Echo with 1>
if not run_test("echo world 1> output2.txt", "output2.txt", "world"):
    sys.exit(1)

# Test 3: Overwrite
with open("output3.txt", "w") as f:
    f.write("old content")
if not run_test("echo new > output3.txt", "output3.txt", "new"):
    sys.exit(1)

# Test 4: External command (ls) - harder to match exact output, so we check if file is not empty
print("Testing: ls > output4.txt")
process = subprocess.Popen(
    [sys.executable, "shell.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True
)
stdout, stderr = process.communicate(input="ls > output4.txt\nexit\n")
if os.path.exists("output4.txt"):
    with open("output4.txt", 'r') as f:
        content = f.read()
    if len(content) > 0:
        print("PASS")
        os.remove("output4.txt")
    else:
        print("FAIL: output4.txt is empty")
        sys.exit(1)
else:
    print("FAIL: output4.txt not created")
    sys.exit(1)

# Test 5: Stderr not redirected
print("Testing: ls nonexistent_file > output5.txt")
process = subprocess.Popen(
    [sys.executable, "shell.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE, # We capture stderr of the shell process, which captures stderr of subprocess if not redirected
    text=True
)
# Note: subprocess.Popen inside shell.py writes to its stderr (which is inherited or printed).
# Since I'm capturing shell.py's stdout/stderr, I should see the error in stdout/stderr of the shell process.
# The internal subprocess inside shell.py inherits stderr from shell.py.
# So if I capture shell.py's stderr, I should see the error there.

stdout, stderr = process.communicate(input="ls nonexistent_file > output5.txt\nexit\n")

# Check file is empty
if os.path.exists("output5.txt"):
    with open("output5.txt", 'r') as f:
        content = f.read()
    if len(content) == 0:
        print("PASS: File is empty")
        os.remove("output5.txt")
    else:
        print(f"FAIL: File is not empty. Content: {content}")
        sys.exit(1)
else:
    print("FAIL: output5.txt not created")
    # Actually, redirection creates the file even if command fails?
    # Yes, standard shell creates the file.
    sys.exit(1)

# Check that error appeared in output (stdout or stderr depending on how shell handles it)
# In my implementation, Executor prints exception to stdout (print f"{command}: execution error: {e}")?
# No, Executor uses subprocess.run. subprocess.run inherits stderr.
# But subprocess.run might fail or print error to stderr.
# Let's check where Executor prints.
# Executor: 
#   except Exception as e: print(f"{command}: execution error: {e}")
# But subprocess.run simply runs. If 'ls' fails, 'ls' writes to stderr.
# 'ls' stderr goes to shell.py's stderr.
# So I should look for "No such file" in stderr (or stdout if captured together).
if "No such file" in stderr or "No such file" in stdout:
    print("PASS: Error message detected")
else:
    print("FAIL: Error message NOT detected in output")
    print("STDOUT:", stdout)
    print("STDERR:", stderr)
    # Note: on some systems ls might print different error.
    # But usually it prints to stderr.
    sys.exit(1)


# Test 6: Append to file
with open("output6.txt", "w") as f:
    f.write("first\n")
if not run_test("echo second >> output6.txt", "output6.txt", "first\nsecond"):
    sys.exit(1)

print("All redirection tests passed.")
