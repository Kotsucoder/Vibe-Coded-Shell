import shlex
from typing import List

class Lexer:
    @staticmethod
    def parse_line(line: str) -> List[str]:
        """
        Parses the command line into arguments, handling single and double quotes.
        """
        args: List[str] = []
        current_token: List[str] = []
        in_single_quote = False
        in_double_quote = False
        in_token = False
        escaped = False

        for char in line:
            if escaped:
                if in_double_quote:
                    if char in ['\\', '"']:
                        current_token.append(char)
                    else:
                        current_token.append('\\')
                        current_token.append(char)
                else:
                    current_token.append(char)
                escaped = False
                in_token = True
            elif in_single_quote:
                if char == "'":
                    in_single_quote = False
                else:
                    current_token.append(char)
            elif in_double_quote:
                if char == '"':
                    in_double_quote = False
                elif char == '\\':
                    escaped = True
                else:
                    current_token.append(char)
            else:
                if char == '\\':
                    escaped = True
                    in_token = True
                elif char == "'":
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
