#!/bin/bash

TIMEFORMAT=%R
PYTHON_CMD="python3.6"
INPUT_FILE="useful.py"
OUTPUT_FILE=""
NUMBER_OF_ITERATIONS=""


# Executes N times the list of program and store the average into the given file
# $1 The file to create and store results in
# $2 The number of
execute_and_average() {
  # Creation of the program to run
  declare -a PROGRAM_TO_RUN=("coroutines.py $INPUT_FILE" "class.py $INPUT_FILE" "nested_loops.py $INPUT_FILE")

  # Delete / Creation of the file
  rm "results-$1" >/dev/null 2>&1
  touch "results-$1" >/dev/null 2>&1

  echo "Processing please wait..."

  # Compute the average
  for ((i = 0; i < ${#PROGRAM_TO_RUN[@]}; i++)); do
    sum=0
    declare -a VALUES=()
    for j in $(seq 1 $2); do
      exec_time=$( { time $PYTHON_CMD ${PROGRAM_TO_RUN[i]} > /dev/null; } 2>&1 )
      VALUES+=($exec_time)
      sum=$(echo "$sum + $exec_time" | bc -l)
    done
    average=$(echo "$sum / $2" | bc -l)

    # Compute the standard deviation
    sum_std=0
    for ((k = 0; k < ${#VALUES[@]}; k++)); do
      sum_std=$(echo "$sum_std + (${VALUES[k]} - $average)^2" | bc -l)
    done
    std=$(echo "sqrt($sum_std / $2)" | bc -l)

    # Compute the standard error mean
    std_err=$(echo "$std / sqrt($2)" | bc -l)

    # Stores the result into the file results-$1
    echo "Average for command: ${PROGRAM_TO_RUN[i]} is $average" >> "results-$1"
    echo "Standard deviation for command: \"${PROGRAM_TO_RUN[i]}\" is $std" >> "results-$1"
    echo "Standard error of the mean for command: \"${PROGRAM_TO_RUN[i]}\" is $std_err" >> "results-$1"
    echo "" >> "results-$1"
  done
  echo "Results stored in results-$1"
}

# Check the given parameters
parameters() {
  # Check for -h
  if [ "$#" -eq 1 ] && [ $1 == "-h" ]; then
    echo "This script is used to launch predefined programs and compute average," \
     "standard deviation and standard error mean over N repetitions"
     echo ""
     echo "USE:"
     echo "    -h: display the help"
     echo "    -o (required): sufix name of the output file (Stores the result). Results are stored in results-FILENAME"
     echo "    -n (required): number of iterations for each program"
     echo "    -i (required): the input file taken as parameters by the programs"
     exit 0
  fi
  # Check the number of parameters
  if [ "$#" -ne 6 ]; then
    echo "Invalid arguments: Results filename(\$1) and number of run(\$2) required."
    echo ""
    echo "Try to use -h (help)"
    exit -1
  fi
  # Check that the second number is a valid integer
  if ! [[ "$2" =~ ^[0-9]+$ ]]; then
    echo "Invalid arguments: The number of run must be a valid integer."
    exit -1
  fi
  # Check that the second number is greater than 0
  if (( $2 == 0 )); then
    echo "Error"
    exit -1
  fi
}

# The first function called for the script
main() {
  parameters "$@"
  execute_and_average $1 $2
  exit 0
}

# Beginning of the script
main "$@"
