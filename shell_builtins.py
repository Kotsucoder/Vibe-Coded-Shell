import os
from typing import List, Dict, Callable
from executor import Executor

class ShellBuiltins:
    def __init__(self):
        self.registry: Dict[str, Callable[[List[str]], bool]] = {}

    def set_registry(self, registry: Dict[str, Callable[[List[str]], bool]]):
        self.registry = registry

    def exit(self, args: List[str]) -> bool:
        """
        Exits the shell.
        """
        return False

    def echo(self, args: List[str]) -> bool:
        """
        Prints the arguments to the console.
        """
        print(" ".join(args))
        return True

    def type(self, args: List[str]) -> bool:
        """
        Determines how a command would be interpreted.
        """
        if not args:
            print("type: missing command argument")
            return True
        
        for command in args:
            if command in self.registry:
                print(f"{command} is a shell builtin")
                continue

            path = Executor.find_in_path(command)
            if path:
                print(f"{command} is {path}")
            else:
                print(f"{command}: not found")
        return True

    def pwd(self, args: List[str]) -> bool:
        """
        Prints the current working directory.
        """
        print(os.getcwd())
        return True

    def cd(self, args: List[str]) -> bool:
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
