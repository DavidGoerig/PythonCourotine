
#########################################################
# @author:  David Goerig                                #
# @id:      djg53                                       #
# @module:  Concurrency and Parallelism - CO890         #
# @asses:   assess 3 - Coroutines in Python             #
# @task:    task2                                       #
#########################################################
###
# desc: compare the fastest way to read a large file (nested loop, classic object programming, coroutines), and show the result in a file
###
import os
import argparse as parse
import time
import math

def manage_args():
    inputfilename = "task1.txt"
    outputfilename = "compare_result.txt"
    iteration = 100
    execoutput = ".outputs_to_delete.txt"
    parser = parse.ArgumentParser()
    parser.add_argument("-f", "-inputfile", type=str, help="arg used for the large file input (default: task1.txt)")
    parser.add_argument("-o", "-outputfile", type=str, help="output file name (default: compare_result.txt)")
    parser.add_argument("-n", "-nbrit", type=int, help="nbr of iteration (default: 100)")
    parser.add_argument("-d", "-execoutput", type=str, help="file for the output, None for stantard output (default: .outputs_to_delete.txt)")
    args = parser.parse_args()
    if args.f:
        inputfilename = args.f
    if args.o:
        outputfilename = args.o
    if args.d:
        execoutput = args.d
    if args.n:
        if args.n <= 0:
            print("Iteration nbr need to be a positive integer")
            return 1
        iteration = args.n
    return inputfilename, outputfilename, iteration, execoutput

def exec_script(dir_path, python_scrit, params, execoutput):
    if execoutput == "None":
        execoutput = ""
    else:
        execoutput = " > " + execoutput
    os.system("python " + dir_path + "/" + python_scrit + " " + params + execoutput)

def exec_them(inputfilename, iteration, execoutput):
    python_file_name = {
        "coroutines": "task4_cobroadcast_with_arg.py",
        "nested_loop": "task3_nested_loop.py",
        "classes": "task2_coroutines_class.py"
    }
    result = {
        "coroutines": [],
        "nested_loop": [],
        "classes": []
    }
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for x in python_file_name:
        for it in range(0, iteration):
            start_time = time.time()
            exec_script(dir_path, python_file_name[x], inputfilename, execoutput)
            result[x].append(time.time() - start_time)
    return result

# calc for each script: the  average,  standard  deviation,  and  the standard error of the mean
def compute_result(results):
    print(results)
    average = {
        "coroutines": 0,
        "nested_loop": 0,
        "classes": 0
    }
    sd = {
        "coroutines": 0,
        "nested_loop": 0,
        "classes": 0
    }
    sem = {
        "coroutines": 0,
        "nested_loop": 0,
        "classes": 0
    }
    for x in results:
        total = 0
        for i in results[x]:
            total += i
        loc_average = total / len(results[x])
        sum_mean_diff = 0
        for i in results[x]:
            sum_mean_diff += pow((i - loc_average), 2)
        loc_sd = math.sqrt(sum_mean_diff / len(results[x]))
        loc_sem = loc_sd / math.sqrt(len(results[x]))
        average[x] = loc_average
        sd[x] = loc_sd
        sem[x] = loc_sem
    return average, sd, sem

def create_file(outputfilename, average, sd, sem, iteration):
    content = ""
    for x in average:
        content += "---------  " + x + " ---------" + "\n"
        content += "Iteration nbr:\t\t\t\t\t" + str(iteration) + "\n"
        content += "Average:\t\t\t\t\t\t" + str(average[x]) + "\n"
        content += "Standard deviation:\t\t\t\t" + str(sd[x]) + "\n"
        content += "Standard error of the mean:\t\t" + str(sem[x]) + "\n" + "\n"
    content += "Fastest method in order according to the average:\n"

    sorted_average = {k: v for k, v in sorted(average.items(), key=lambda item: -item[1], reverse=True)}
    last = 0
    for x in sorted_average:
        diff = ""
        if (last != 0):
            diff = " (" + str(((sorted_average[x] - last) / last) * 100) + " % more than the previous one)."
        last = sorted_average[x]
        content += x + "\t->\t" + str(sorted_average[x]) + diff + "\n"
    content += "\nLess deviation from the average (standard deviation):\n"
    sorted_sd = {k: v for k, v in sorted(sd.items(), key=lambda item: -item[1], reverse=True)}
    last = 0
    for x in sorted_sd:
        diff = ""
        if (last != 0):
            diff = " (" + str(((sorted_sd[x] - last) / last) * 100) + " % more than the previous one)."
        last = sorted_sd[x]
        content += x + "\t->\t" + str(sorted_sd[x]) + diff +  "\n"
    content += "\nMost homogeneous method in order (standard error to the mean):\n"
    sorted_sem = {k: v for k, v in sorted(sem.items(), key=lambda item: -item[1], reverse=True)}
    last = 0
    for x in sorted_sem:
        diff = ""
        if last != 0:
            diff = " (" + str(((sorted_sem[x] - last) / last) * 100) + " % more than the previous one)."
        last = sorted_sem[x]
        content += x + "\t->\t" + str(sorted_sem[x]) + diff +  "\n"
    f = open(outputfilename, "w")
    f.write(content)
    f.close()

def main():
    inputfilename, outputfilename, iteration, execoutput = manage_args()
    try:
        open(inputfilename)
    except FileNotFoundError as error:
        print("Error: " + str(error))
        return 1
    results = exec_them(inputfilename, iteration, execoutput)
    average, sd, sem = compute_result(results)
    create_file(outputfilename, average, sd, sem, iteration)
    return 0

if __name__ == '__main__':
    exit(main())
