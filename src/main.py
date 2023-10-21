import os
import time
import threading
import random


class Node:
    def __init__(self, state, parent, action, depth):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth
        self.f = 0


class Puzzle:
    def __init__(self, initial_state):
        self.initial_state = initial_state
        self.goal_state = [0, 1, 2, 3, 4, 5, 6, 7, 8]
        self.unique_states = set()

    def goal_test(self, state):
        return state == self.goal_state

    def get_successors(self, state):
        successors = []
        zero_index = state.index(0)

        actions = {"UP": -3, "DOWN": 3, "LEFT": -1, "RIGHT": 1}
        for action in actions:
            target_index = zero_index + actions[action]
            if (action in ["UP", "DOWN"] and 0 <= target_index < len(state)) or \
                    (action == "LEFT" and zero_index % 3 != 0) or \
                    (action == "RIGHT" and zero_index % 3 != 2):
                new_state = state.copy()
                new_state[zero_index], new_state[target_index] = new_state[target_index], new_state[zero_index]
                successors.append((new_state, action))
                self.unique_states.add(tuple(new_state))

        return successors


class DLS:
    def __init__(self, puzzle, limit):
        self.puzzle = puzzle
        self.limit = limit
        self.node_count = 0

    def search(self):
        return self.recursive_dls(Node(self.puzzle.initial_state, None, "INIT ", 0), self.limit)

    def recursive_dls(self, node, limit):
        self.node_count += 1
        if self.puzzle.goal_test(node.state):
            return node
        elif node.depth == limit:
            return 'cutoff'
        else:
            cutoff_occurred = False
            for child in self.puzzle.get_successors(node.state):
                result = self.recursive_dls(Node(child[0], node, child[1], node.depth + 1), limit)
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
            return 'cutoff' if cutoff_occurred else 'failure'


class RBFS:
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.node_count = 0

    def search(self):
        start_node = Node(self.puzzle.initial_state, None, "INIT", 0)
        start_node.f = self.manhattan_distance(start_node.state)
        return self.rbfs(start_node, float('inf'))

    def rbfs(self, node, f_limit):
        successors = []
        if self.puzzle.goal_test(node.state):
            return node, node.f
        children = self.puzzle.get_successors(node.state)
        if not children:
            return None, float('inf')
        for child in children:
            new_node = Node(child[0], node, child[1], node.depth + 1)
            new_node.f = max(new_node.depth + self.manhattan_distance(new_node.state), node.f)
            successors.append(new_node)
        self.node_count += 1
        while True:
            successors.sort(key=lambda x: x.f)
            best = successors[0]
            if best.f > f_limit:
                return None, best.f
            if len(successors) > 1:
                alternative = successors[1].f
            else:
                alternative = float('inf')
            result, best.f = self.rbfs(best, min(f_limit, alternative))
            if result is not None:
                return result, best.f

    def manhattan_distance(self, state):
        distance = 0
        for i in range(1, 9):
            xs, ys = divmod(state.index(i), 3)
            xg, yg = divmod(self.puzzle.goal_state.index(i), 3)
            distance += abs(xs - xg) + abs(ys - yg)
        return distance


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
    return len(path)


def read_puzzle_from_file(filename):
    with open(filename, 'r') as file:
        puzzle = list(map(int, file.read().split(',')))
    return puzzle


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


def main():
    initial_state = [8, 7, 6, 0, 4, 1, 2, 5, 3]
    print(initial_state)
    puzzle = Puzzle(initial_state)
    # dls = DLS(puzzle, 22)
    rbfs = RBFS(puzzle)

    def run_search():
        print("Solving started")
        start_time = time.time()
        # result = dls.search()
        result = rbfs.search()
        print("--- %s seconds ---" % (time.time() - start_time))
        print(result)

        states_in_memory = print_path(result[0])
        if states_in_memory is not None:
            # print(f"Number of iterations: {dls.node_count}")
            print(f"Number of iterations: {rbfs.node_count}")
            print(f"Number of states: {len(puzzle.unique_states)}")
            print(f"Number of states in memory: {states_in_memory}")

    search_thread = threading.Thread(target=run_search)
    search_thread.start()
    search_thread.join(30 * 60)
    if search_thread.is_alive():
        print("Search exceeded time limit")
        os.abort()


main()
