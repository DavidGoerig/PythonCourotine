
#########################################################
# @author:  David Goerig                                #
# @id:      djg53                                       #
# @module:  Concurrency and Parallelism - CO890         #
# @asses:   assess 3 - Coroutines in Python             #
# @task:    task3                                       #
#########################################################
###
# desc: all the function to print the file in the main
###
import sys


if __name__ == "__main__":
    filename = "task1.txt"
    if len(sys.argv) == 2:
        if sys.argv[1] == "-h":
            print("USAGE:\n\t- 0 arg: task1.txt is use as large file\n\t- 1 arg: arg used as large file")
            exit(0)
        else:
            filename = sys.argv[1]
    elif len(sys.argv) > 2:
        print("Too much argument, -h for help")
        exit(1)
    patterns = {"python", "CRON", "systemd"}
    try:
        the_file = open(filename)
    except FileNotFoundError as error:
        print("Error: " + str(error))
        exit(1)
    line = the_file.readline()
    while line:
        if len(line.strip()) > 0:
            for pattern in patterns:
                if pattern in line:
                    print(line)
        line = the_file.readline()
    exit(0)
