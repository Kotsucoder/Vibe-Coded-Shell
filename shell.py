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

    def _parse_redirection(self, parts: List[str]) -> Tuple[Optional[List[str]], Optional[str]]:
        """
        Parses the command parts for output redirection.
        Returns a tuple of (cleaned_parts, output_file_path).
        """
        output_file_path = None
        cleaned_parts = []
        skip_next = False
        
        for i, part in enumerate(parts):
            if skip_next:
                skip_next = False
                continue
                
            if part in [">", "1>"]:
                if i + 1 < len(parts):
                    output_file_path = parts[i + 1]
                    skip_next = True
                else:
                    print("Syntax error: expected file path after redirection operator")
                    return None, None
            else:
                cleaned_parts.append(part)
                
        return cleaned_parts, output_file_path

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
                
                cleaned_parts, output_file_path = self._parse_redirection(parts)
                if cleaned_parts is None:
                    continue
                
                parts = cleaned_parts
                output_file = None

                if output_file_path:
                    try:
                        output_file = open(output_file_path, 'w')
                    except Exception as e:
                        print(f"Error opening file: {e}")
                        continue

                try:
                    if not parts:
                        # If there's no command but redirection, we've already opened (and truncated) the file.
                        continue

                    command = parts[0]
                    args = parts[1:]

                    if command in self.builtins:
                        if output_file:
                            old_stdout = sys.stdout
                            sys.stdout = output_file
                            try:
                                if not self.builtins[command](args):
                                    break
                            finally:
                                sys.stdout = old_stdout
                        else:
                            if not self.builtins[command](args):
                                break
                    else:
                        Executor.run_external_program(command, args, output_file=output_file)
                finally:
                    if output_file:
                        output_file.close()
                    
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
