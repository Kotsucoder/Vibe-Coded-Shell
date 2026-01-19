import os
import subprocess
from typing import List, Optional

class Executor:
    @staticmethod
    def find_in_path(command: str) -> Optional[str]:
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

    @staticmethod
    def run_external_program(command: str, args: List[str]) -> bool:
        """
        Runs an external program.
        """
        program_path = Executor.find_in_path(command)
        if program_path:
            try:
                # Pass the arguments from command line to the program
                # We use the original command name as argv[0] to be polite, 
                # but execute the specific file we found.
                subprocess.run([command] + args, executable=program_path)
            except Exception as e:
                print(f"{command}: execution error: {e}")
        else:
            print(f"{command}: command not found")
        return True
