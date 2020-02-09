
#########################################################
# @author:  David Goerig                                #
# @id:      djg53                                       #
# @module:  Concurrency and Parallelism - CO890         #
# @asses:   assess 3 - Coroutines in Python             #
# @task:    task2                                       #
#########################################################
###
# desc: all the function without coroutines in classes
###
import sys

##
# param:    thefile: file descriptor of the file to read, target: the target class to follow
# desc:     this class read the fine line by line and call the class to print
##


class Follow:
    def __init__(self, thefile, target):
        self._thefile = thefile
        self._target = target

    def follow(self):
        line = self._thefile.readline()
        while line:
            if (len(line.strip()) != 0):
                self._target.do(line)
            line = self._thefile.readline()

##
# desc:     class receiving data and printing it
##


class Printer:
    def printit(self, to_print):
        print(to_print)
##
# param:    pattern: pattern to search, target: the target class (printer in this case)
# desc:     check and filter the lines matching the patterns
##


class Grep:
    def __init__(self, pattern, target):
        self._pattern = pattern
        self._target = target

    def grep(self, line):
        if self._pattern in line:
            self._target.printit(line)

##
# param:    target: target list to call
# desc:     send to each functions
##


class Broadcast:
    def __init__(self, targets):
        self._targets = targets

    def do(self, item):
        for target in self._targets:
            target.grep(item)

##
#   main
##


if __name__ == "__main__":
    filename = "task1.txt"
    if (len(sys.argv) == 2):
        if sys.argv[1] == "-h":
            print("USAGE:\n\t- 0 arg: task1.txt is use as large file\n\t- 1 arg: arg used as large file")
            exit(0)
        else:
            filename = sys.argv[1]
    elif (len(sys.argv) > 2):
        print("Too much argument, -h for help")
        exit(1)
    printer = Printer()
    broadcast = Broadcast(
        {
        Grep("python", printer),
        Grep("CRON", printer),
        Grep("systemd", printer)
        }
    )
    try:
        the_file = open(filename)
    except FileNotFoundError as error:
        print("Error: " + str(error))
        exit(1)
    follow = Follow(the_file, broadcast)
    follow.follow()
    exit(0)