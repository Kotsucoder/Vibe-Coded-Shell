#!/usr/bin/env python3

import sys
from typing import Dict, Callable, List
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
                
                command = parts[0]
                args = parts[1:]

                if command in self.builtins:
                    if not self.builtins[command](args):
                        break
                else:
                    Executor.run_external_program(command, args)
                    
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
