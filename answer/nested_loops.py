import useful
from sys import argv

# @author Bastien Lecussan
# This program is made for python 3.6
# This code follow the Pep8 python guide code style
# This code use Typing Hint (Python 3.5 >) to type variables

ERROR_CODE_EXIT = -1
SUCCESS_CODE_EXIT = 0

def main() -> int:
    """
    Main function used by the program as entrypoint
    Read a file look for patterns and print them to the output
    :return: The value to exit
    """
    if (len(argv) != 2):
        useful.eprint("Invalid args: Filename required as input (Path).")
        return ERROR_CODE_EXIT

    pattern_list = { "python", "CRON", "systemd" }
    try:
        fd = open(argv[1])
    except FileNotFoundError as err:
        useful.eprint("Exception: " + str(err))
        useful.eprint("Program: File \"" + argv[1] + "\" not found.")
        return ERROR_CODE_EXIT

    line = fd.readline()
    while line:
        if len(line.strip()) > 0:
            for pattern in pattern_list:
                if pattern in line:
                    print(line)
        line = fd.readline()

    return SUCCESS_CODE_EXIT

# Detection of the beginning of the program
if __name__ == "__main__":
    exit(main())
