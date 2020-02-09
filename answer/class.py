import useful
from sys import argv

# @author Bastien Lecussan
# This program is made for python 3.6
# This code follow the Pep8 python guide code style
# This code use Typing Hint (Python 3.5 >) to type variables

ERROR_CODE_EXIT = -1
SUCCESS_CODE_EXIT = 0

class Printer:
    """
    Printer used to print lines
    """
    def work(self, line: str) -> None:
        """
        Print a line given as parameter
        :param line: The line to print
        :return: None
        """
        print(line)

Printer.__doc__ = "(Instance) Printer()\n" \
                  + "Object that can print lines\n" \
                  + "Methods:\n" \
                  + "work(line: str) -> None; Print the given line\n"

class Grep:
    """
    Grep object used to reproduce grep command line behaviour
    """
    def __init__(self, pattern: str, printer: Printer) -> None:
        """
        This is the constructor of the object
        :param pattern: The pattern to look for
        :param printer: The printer to call once a pattern is detected
        """
        self._pattern = pattern
        self._printer = printer

    def work(self, line: str) -> None:
        """
        Look for the pattern of the object and print the line if it finds it.
        :param line: The line to look for the _pattern
        :return: None
        """
        if self._pattern in line:
            self._printer.work(line)

Grep.__doc__ = "(Instance) Grep(pattern: str, printer: Printer)\n" \
               + "Object which reproduces grep behavior\n" \
               + "Methods:\n" \
               + "work(line: str) -> None; Find a pattern and if find, print the line\n"

class Broadcast:
    """
    This send the different lines to the different targets in order to be
    computed
    """
    def __init__(self, targets: list) -> None:
        """
        Constructor
        :param targets: List of targets to call to process the data received
        """
        self._targets = targets

    def work(self, line: str) -> None:
        """
        Send the received line to the different targets
        :param line:
        :return: None
        """
        for target in self._targets:
            target.work(line)

Broadcast.__doc__ = "(Instance) Broadcast(targets: list)\n" \
                    + "This class send received line to the different targets to be computed\n" \
                    + "Methods:\n" \
                    + "work(line: str) -> None; Send the received line to the different targets\n"

class Follow:
    """
    Used to read and send line to the target (Broadcaster)
    """
    def __init__(self, filename: str, broadcast: Broadcast) -> None:
        """

        :param filename: The filename of the file to read
        :param broadcast: The broadcaster
        :raise FileNotFoundError: File not found exception
        """
        self._broadcast = broadcast
        try:
            self._fd = open(filename)
        except FileNotFoundError as e:
            self._fd = None
            raise e

    def work(self) -> None:
        """
        Read the file descriptor opened from the file and
        sends line to the broadcaster
        :return: None
        """
        line = self._fd.readline()
        while line:
            if len(line.strip()) > 0:
                self._broadcast.work(line)
            line = self._fd.readline()

    def __del__(self) -> None:
        """
        Destructor of the object
        :return: None
        """
        if self._fd != None:
            self._fd.close()

Follow.__doc__ = "(Instance) Follow(filename: str, target: Broadcast)\n"\
    + "This function is used to read and send the line to the target (broadcaster)" \
    + "Methods:\n" \
    + "work() -> None; Read the file and send lines to the broadcaster\n"

def main() -> int:
    """
    Main function used by the program as entrypoint
    :return: The value to exit
    """
    if (len(argv) != 2):
        useful.eprint("Invalid args: Filename required as input (Path).")
        return ERROR_CODE_EXIT

    printer_class = Printer()
    tab_grep = {
        Grep("python", printer_class),
        Grep("CRON", printer_class),
        Grep("systemd", printer_class)
    }
    broadcast_class = Broadcast(tab_grep)
    try:
        follow_class = Follow(argv[1], broadcast_class)
    except Exception as err:
        useful.eprint("Exception: " + str(err))
        useful.eprint("Program: File \"" + argv[1] + "\" not found.")
        return ERROR_CODE_EXIT
    follow_class.work()
    return SUCCESS_CODE_EXIT

# Detection of the beginning of the program
if __name__ == "__main__":
    exit(main())
