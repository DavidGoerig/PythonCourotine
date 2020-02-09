# An example of broadcasting a data stream onto multiple
# coroutine targets. with input argument (modified by David Goerig)
# https://github.com/shitangdama/coroutines/blob/master/cobroadcast.py

import time
import sys

# A data source. This function reads the file line by line
# and sends the lines to the "target" coroutine.
def follow(thefile, target):
    target.send(None) # prime the target coroutine
    while True:
         line = thefile.readline()
         if not line:
             time.sleep(0.5)
             break
         if len(line.strip()) == 0:
             continue
         target.send(line)

# Only lines that match the pattern are sent to
# the target coroutine.
def grep(pattern, target):
    target.send(None)
    while True:
        line = (yield)  # Receive a line
        if pattern in line:
            target.send(line) # Send to next stage


# A coroutine that receives data and prints it
def printer():
    while True:
         line = (yield)
         print(line)

# Broadcast a stream onto multiple targets
def broadcast(targets):
    for target in targets:
        target.send(None)
    while True:
        item = (yield)
        for target in targets:
            target.send(item)

# Example wiring
if __name__ == '__main__':
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
    try:
        f = open(filename)
    except FileNotFoundError as error:
        print("Error: " + str(error))
        exit(1)
    follow(f,
       broadcast([grep('python',printer()),
                  grep('CRON',printer()),
                  grep('systemd',printer())])
           )
