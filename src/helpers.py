import random
import time
import os
from solving_methods import *


def print_path(result):
    def print_state(act, st):
        max_len = 5
        for i in range(0, len(st), 3):
            if i == 3:
                print(f'{act:{max_len}}', st[i:i + 3])
            else:
                print(f'{"":{max_len}}', st[i:i + 3])
        print()

    if result == 'cutoff' or result == 'failure':
        print("No solution found within the given limit.")
        return None
    path = []
    while result:
        path.append((result.state, result.action))
        result = result.parent
    for state, action in reversed(path):
        print_state(action, state)
    return len(path) - 1


def read_matrix(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"No such file: '{file_path}'")
    with open(file_path, 'r') as file:
        lines = file.readlines()
    unique_numbers = set()
    numbers = []
    for line in lines:
        line_numbers = line.strip().split()
        for number in line_numbers:
            if not number.isdigit() or int(number) < 0 or int(number) > 8:
                raise ValueError(f"Invalid number {number} in file")
            unique_numbers.add(int(number))
            numbers.append(int(number))
    if len(unique_numbers) != 9:
        raise ValueError("Not all numbers from 0 to 8 are present in the file")
    return numbers


def generate_puzzle():
    puzzle = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    random.shuffle(puzzle)
    while not is_solvable(puzzle):
        random.shuffle(puzzle)
    return puzzle


def is_solvable(puzzle):
    inversions = 0
    for i in range(len(puzzle)):
        for j in range(i+1, len(puzzle)):
            if puzzle[i] != 0 and puzzle[j] != 0 and puzzle[i] > puzzle[j]:
                inversions += 1
    return inversions % 2 == 0


def run_search(puzzle, method, limit_dls=0):
    print("Solving started")
    if method == "RBFS":
        rbfs = RBFS(puzzle)
        start_time = time.time()
        result = rbfs.search()
        solving_time = time.time() - start_time

        steps = print_path(result[0])
        if steps is not None:
            print(f"Solving took {steps} steps")
            print(f"Solving took {solving_time} seconds")
            print(f"Number of iterations: {rbfs.node_count}")
            print(f"Number of states: {len(puzzle.unique_states)}")
            print(f"Number of states in memory: {rbfs.max_nodes_in_memory}")
    else:
        dls = DLS(puzzle, limit_dls)
        start_time = time.time()
        result = dls.search()
        solving_time = time.time() - start_time

        steps = print_path(result)
        if steps is not None:
            print(f"Solving took {steps} steps")
            print(f"Solving took {solving_time} seconds")
            print(f"Number of iterations: {dls.node_count}")
            print(f"Number of states: {len(puzzle.unique_states)}")
            print(f"Number of states in memory: {dls.max_nodes_in_memory}")


def is_choice_num(choice):
    if choice == '1':
        return True
    elif choice == '0':
        return False
    return None


def validate_positive_integer(n):
    try:
        value = int(n)
        if value > 0:
            return True
        else:
            return False
    except ValueError:
        return False


def print_matrix(arr):
    for i in range(0, 9, 3):
        print(arr[i:i + 3])
