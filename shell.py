#!/usr/bin/env python3

import sys

class Shell:
    def __init__(self):
        self.builtins = {
            "exit": self.builtin_exit,
            "echo": self.builtin_echo,
        }

    def builtin_exit(self, *args):
        """
        Exits the shell.
        """
        return False

    def builtin_echo(self, *args):
        """
        Prints the arguments to the console.
        """
        print(" ".join(args))
        return True

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
                parts = line.split()
                command = parts[0]
                args = parts[1:]

                if command in self.builtins:
                    if not self.builtins[command](*args):
                        break
                else:
                    print(f"{command}: command not found")
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