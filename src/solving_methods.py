from abc import ABC, abstractmethod
from node import *


class SolvingMethod(ABC):
    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.node_count = 0
        self.max_nodes_in_memory = 0

        super().__init__()

    @abstractmethod
    def search(self):
        pass


class DLS(SolvingMethod):
    def __init__(self, puzzle, limit):
        super().__init__(puzzle)
        self.limit = limit
        self.nodes_at_depth = [0] * (limit + 1)

    def search(self):
        return self.recursive_dls(Node(self.puzzle.initial_state, None, "INIT", 0))

    def recursive_dls(self, node):
        self.node_count += 1
        cutoff_occurred = False
        if self.puzzle.goal_test(node.state):
            self.max_nodes_in_memory = max(self.max_nodes_in_memory, sum(self.nodes_at_depth))
            return node
        elif node.depth == self.limit:
            self.max_nodes_in_memory = max(self.max_nodes_in_memory, sum(self.nodes_at_depth))
            self.nodes_at_depth[node.depth] = 0
            return 'cutoff'
        else:
            children = self.puzzle.get_successors(node.state)
            self.nodes_at_depth[node.depth] = len(children)
            for child in children:
                result = self.recursive_dls(Node(child[0], node, child[1], node.depth + 1))
                if result == 'cutoff':
                    cutoff_occurred = True
                elif result is not None:
                    return result
            return 'cutoff' if cutoff_occurred else 'failure'


class RBFS(SolvingMethod):
    def __init__(self, puzzle):
        super().__init__(puzzle)
        self.current_nodes_in_memory = 0

    def search(self):
        start_node = Node(self.puzzle.initial_state, None, "INIT", 0)
        start_node.f = self.manhattan_distance(start_node.state)
        return self.rbfs(start_node, float('inf'))

    def rbfs(self, node, f_limit):
        self.max_nodes_in_memory = max(self.max_nodes_in_memory, self.current_nodes_in_memory)
        if self.puzzle.goal_test(node.state):
            return node, node.f
        successors = []
        children = self.puzzle.get_successors(node.state)
        if not children:
            return None, float('inf')
        for child in children:
            new_node = Node(child[0], node, child[1], node.depth + 1)
            new_node.f = max(new_node.depth + self.manhattan_distance(new_node.state), node.f)
            successors.append(new_node)
            self.node_count += 1
            self.current_nodes_in_memory += 1
        while True:
            successors.sort(key=lambda x: x.f)
            best = successors[0]
            if best.f > f_limit:
                self.current_nodes_in_memory -= (len(successors) - 0)
                return None, best.f
            alternative = successors[1].f if len(successors) > 1 else float('inf')
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
