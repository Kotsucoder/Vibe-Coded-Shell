#!/usr/bin/env python3

import sys
from typing import Dict, Callable, List, Tuple, Optional
from lexer import Lexer
from executor import Executor
from shell_builtins import ShellBuiltins

class Shell:
    def __init__(self):
        self.builtins_handler = ShellBuiltins()
        self.builtins: Dict[str, Callable[[List[str]], bool]] = {
            "exit": self.builtins_handler.exit,
            "echo": self.builtins_handler.echo,
            "type": self.builtins_handler.type,
            "pwd": self.builtins_handler.pwd,
            "cd": self.builtins_handler.cd,
        }
        self.builtins_handler.set_registry(self.builtins)

    def _parse_redirection(self, parts: List[str]) -> Tuple[Optional[List[str]], Optional[str], Optional[str], bool]:
        """
        Parses the command parts for output and error redirection.
        Returns a tuple of (cleaned_parts, output_file_path, error_file_path, append_mode).
        """
        output_file_path = None
        error_file_path = None
        cleaned_parts = []
        skip_next = False
        append_mode = False
        
        for i, part in enumerate(parts):
            if skip_next:
                skip_next = False
                continue
                
            if part in [">", "1>"]:
                if i + 1 < len(parts):
                    output_file_path = parts[i + 1]
                    skip_next = True
                    append_mode = False
                else:
                    print("Syntax error: expected file path after redirection operator")
                    return None, None, None, False
            elif part in [">>", "1>>"]:
                if i + 1 < len(parts):
                    output_file_path = parts[i + 1]
                    skip_next = True
                    append_mode = True
                else:
                    print("Syntax error: expected file path after redirection operator")
                    return None, None, None, False
            elif part == "2>":
                if i + 1 < len(parts):
                    error_file_path = parts[i + 1]
                    skip_next = True
                else:
                    print("Syntax error: expected file path after stderr redirection operator")
                    return None, None, None, False
            else:
                cleaned_parts.append(part)
                
        return cleaned_parts, output_file_path, error_file_path, append_mode

    def run(self):
        """
        Main loop to run the Vibe Coded Shell.
        """
        while True:
            try:
                print("$ ", end="", flush=True)
                line = sys.stdin.readline()
                if not line:
                    break
                line = line.strip()
                if not line:
                    continue
                
                parts = Lexer.parse_line(line)
                if not parts:
                    continue
                
                cleaned_parts, output_file_path, error_file_path, append_mode = self._parse_redirection(parts)
                if cleaned_parts is None:
                    continue
                
                parts = cleaned_parts
                output_file = None
                error_file = None

                if output_file_path:
                    try:
                        mode = 'a' if append_mode else 'w'
                        output_file = open(output_file_path, mode)
                    except Exception as e:
                        print(f"Error opening file: {e}")
                        continue

                if error_file_path:
                    try:
                        error_file = open(error_file_path, 'w')
                    except Exception as e:
                        print(f"Error opening stderr file: {e}")
                        if output_file:
                            output_file.close()
                        continue

                try:
                    if not parts:
                        # If there's no command but redirection, we've already opened (and truncated) the file.
                        continue

                    command = parts[0]
                    args = parts[1:]

                    if command in self.builtins:
                        old_stdout = sys.stdout
                        old_stderr = sys.stderr
                        try:
                            if output_file:
                                sys.stdout = output_file
                            if error_file:
                                sys.stderr = error_file
                            
                            if not self.builtins[command](args):
                                break
                        finally:
                            sys.stdout = old_stdout
                            sys.stderr = old_stderr
                    else:
                        Executor.run_external_program(command, args, output_file=output_file, error_file=error_file)
                finally:
                    if output_file:
                        output_file.close()
                    if error_file:
                        error_file.close()
            except KeyboardInterrupt:
                print()
                continue

def main():
    """
    Main function to run the Vibe Coded Shell.
    """
    shell = Shell()
    shell.run()

if __name__ == "__main__":
    main()
