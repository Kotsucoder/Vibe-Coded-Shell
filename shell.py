#!/usr/bin/env python3

import sys
import os

class Shell:
    def __init__(self):
        self.builtins = {
            "exit": self.builtin_exit,
            "echo": self.builtin_echo,
            "type": self.builtin_type,
            "pwd": self.builtin_pwd,
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

    def builtin_type(self, *args):
        """
        Determines how a command would be interpreted.
        """
        if not args:
            print("type: missing command argument")
            return True
        
        for command in args:
            if command in self.builtins:
                print(f"{command} is a shell builtin")
                continue

            path_dirs = os.environ.get("PATH", "").split(os.pathsep)
            found = False
            for directory in path_dirs:
                file_path = os.path.join(directory, command)
                if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
                    print(f"{command} is {file_path}")
                    found = True
                    break
            
            if not found:
                print(f"{command}: not found")
        return True

    def builtin_pwd(self, *args):
        """
        Prints the current working directory.
        """
        print(os.getcwd())
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