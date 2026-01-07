#!/usr/bin/env python3

def main():
    """
    Main function to run the Vibe Coded Shell.
    """
    while True:
        print("$ ", end="")
        command = input()
        print(f"{command}: command not found")

if __name__ == "__main__":
    main()
