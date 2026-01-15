#!/usr/bin/env python3

import sys
import os
import subprocess

class Shell:
    def __init__(self):
        self.builtins = {
            "exit": self.builtin_exit,
            "echo": self.builtin_echo,
            "type": self.builtin_type,
            "pwd": self.builtin_pwd,
            "cd": self.builtin_cd,
        }

    def find_in_path(self, command):
        """
        Searches for a command in the PATH environment variable.
        Returns the full path to the executable if found, otherwise None.
        """
        path_dirs = os.environ.get("PATH", "").split(os.pathsep)
        for directory in path_dirs:
            file_path = os.path.join(directory, command)
            if os.path.isfile(file_path) and os.access(file_path, os.X_OK):
                return file_path
        return None

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

            path = self.find_in_path(command)
            if path:
                print(f"{command} is {path}")
            else:
                print(f"{command}: not found")
        return True

    def builtin_pwd(self, *args):
        """
        Prints the current working directory.
        """
        print(os.getcwd())
        return True

    def builtin_cd(self, *args):
        """
        Changes the current working directory.
        """
        if not args:
            return True

        path = args[0]
        if path.startswith("~"):
            home = os.environ.get("HOME")
            if home is None:
                print("cd: HOME not set")
                return True
            
            if path == "~":
                path = home
            elif path.startswith("~/"):
                path = os.path.join(home, path[2:])

        try:
            os.chdir(path)
        except FileNotFoundError:
            print(f"cd: {path}: No such file or directory")
        except Exception:
             print(f"cd: {path}: No such file or directory")
        return True

    def parse_line(self, line):
        """
        Parses the command line into arguments, handling single and double quotes.
        """
        args = []
        current_token = []
        in_single_quote = False
        in_double_quote = False
        in_token = False

        for char in line:
            if in_single_quote:
                if char == "'":
                    in_single_quote = False
                else:
                    current_token.append(char)
            elif in_double_quote:
                if char == '"':
                    in_double_quote = False
                else:
                    current_token.append(char)
            else:
                if char == "'":
                    in_single_quote = True
                    in_token = True
                elif char == '"':
                    in_double_quote = True
                    in_token = True
                elif char.isspace():
                    if in_token:
                        args.append("".join(current_token))
                        current_token = []
                        in_token = False
                else:
                    current_token.append(char)
                    in_token = True
        
        if in_token:
            args.append("".join(current_token))
            
        return args

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
                parts = self.parse_line(line)
                if not parts:
                    continue
                command = parts[0]
                args = parts[1:]

                if command in self.builtins:
                    if not self.builtins[command](*args):
                        break
                else:
                    program_path = self.find_in_path(command)
                    if program_path:
                        try:
                            # Pass the arguments from command line to the program
                            # We use the original command name as argv[0] to be polite, 
                            # but execute the specific file we found.
                            subprocess.run([command] + list(args), executable=program_path)
                        except Exception as e:
                            print(f"{command}: execution error: {e}")
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