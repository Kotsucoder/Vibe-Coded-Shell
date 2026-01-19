#!/usr/bin/env python3

import sys
import os
import json
import io
import unittest
from typing import List, Any, Dict
from lexer import Lexer
from shell import Shell

class TestRunner(unittest.TestCase):
    def run_tests(self, test_file: str):
        with open(f"tests/{test_file}.json", 'r') as f:
            data = json.load(f)

        print(f"Running tests from {test_file}.json...")
        
        for test_case in data:
            name = test_case.get("name")
            test_type = test_case.get("type")
            input_data = test_case.get("input")
            expected = test_case.get("expected")

            print(f"  Running {name}...", end=" ")
            
            try:
                if test_type == "parse":
                    result = Lexer.parse_line(input_data)
                    self.assertEqual(result, expected)
                elif test_type == "run":
                    # Setup mocks
                    held_stdout = sys.stdout
                    held_stdin = sys.stdin
                    stdout = io.StringIO()
                    stdin = io.StringIO(input_data)
                    sys.stdout = stdout
                    sys.stdin = stdin
                    
                    try:
                        shell = Shell()
                        shell.run()
                    except SystemExit:
                        pass
                    finally:
                        sys.stdout = held_stdout
                        sys.stdin = held_stdin

                    output = stdout.getvalue()
                    if isinstance(expected, list):
                         for exp_str in expected:
                             self.assertIn(exp_str, output)
                    else:
                        self.assertIn(expected, output)
                else:
                    print(f"Unknown test type: {test_type}")
                    continue
                
                print("PASS")
            except AssertionError as e:
                print(f"FAIL")
                print(f"    Expected: {expected}")
                print(f"    Got: {result if test_type == 'parse' else output}")
                print(f"    Error: {e}")
            except Exception as e:
                print(f"ERROR: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ./unit_tests.py <test_name>")
        sys.exit(1)
    
    test_name = sys.argv[1]
    runner = TestRunner()
    runner.run_tests(test_name)
