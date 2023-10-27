import threading
from puzzle import *
from helpers import *
from memory_limiter import *


def main():
    file_name = "input.txt"
    memory_limit = 1024 * 1024 * 1024
    time_limit = 30 * 60

    while True:
        puzzle_choice = input("Random puzzle or from txt file?(1/0):")
        puzzle_choice = is_choice_num(puzzle_choice)
        if puzzle_choice is not None:
            break
    if puzzle_choice:
        initial_state = generate_puzzle()
    else:
        initial_state = read_matrix(file_name)
        if not is_solvable(initial_state):
            print(f"Puzzle read from file is not solvable")
            return
    print_matrix(initial_state)
    puzzle = Puzzle(initial_state)

    assign_job(create_job())
    limit_memory(memory_limit)
    try:
        while True:
            solution_choice = input("RBFS or LDFS?(1/0):")
            solution_choice = is_choice_num(solution_choice)
            if solution_choice is not None:
                break
        if solution_choice:
            search_thread = threading.Thread(target=run_search, args=(puzzle, "RBFS"))
        else:
            while True:
                limit = input("Enter LDFS depth limit:")
                if validate_positive_integer(limit):
                    break
            search_thread = threading.Thread(target=run_search, args=(puzzle, "LDFS", int(limit)))

        search_thread.start()
        search_thread.join(time_limit)
        if search_thread.is_alive():
            print("Search exceeded time limit")
            os.abort()
    except (MemoryError, RuntimeError):
        print('Memory ran out')
    return 0


main()
