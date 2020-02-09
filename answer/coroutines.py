# An example of broadcasting a data stream onto multiple
# coroutine targets.
# https://github.com/shitangdama/coroutines/blob/master/cobroadcast.py

import time
from sys import argv
import useful

# A data source. This function reads the file line by line
# and sends the lines to the "target" coroutine.
def follow(thefile, target):
    target.send(None) # prime the target coroutine
    while True:
         line = thefile.readline()
         if not line:
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
    if (len(argv) != 2):
        useful.eprint("Invalid args: Filename required as input (Path).")
        exit(-1)

    try:
        f = open(argv[1])
    except FileNotFoundError as err:
        useful.eprint("Exception: " + str(err))
        useful.eprint("Program: File \"" + argv[1] + "\" not found.")
        exit(-1)
    follow(f,
       broadcast([grep('python',printer()),
                  grep('CRON',printer()),
                  grep('systemd',printer())])
           )
    f.close()
    exit(0)
