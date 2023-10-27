import unittest
from solving_methods import *
from puzzle import *


class TestDLS(unittest.TestCase):
    def test_negative(self):
        print("DLS tests")
        self.puzzle = Puzzle([2, 1, 3, 4, 5, 6, 7, 8, 0])
        node = Node(self.puzzle.initial_state, None, "INIT", 0)
        self.dls = DLS(self.puzzle, 3)
        result = self.dls.recursive_dls(node)
        self.assertEqual(result, 'cutoff')

    def test_positive(self):
        self.puzzle = Puzzle([1, 2, 3, 4, 5, 6, 7, 0, 8])
        node = Node(self.puzzle.initial_state, None, "INIT", 0)
        self.dls = DLS(self.puzzle, 1)
        result = self.dls.recursive_dls(node)
        self.assertEqual(result.state, self.puzzle.goal_state)

    def test_edge_values_1(self):
        self.puzzle = Puzzle([1, 2, 6, 7, 5, 4, 0, 8, 3])
        node = Node(self.puzzle.initial_state, None, "INIT", 0)
        self.dls = DLS(self.puzzle, 18)
        result = self.dls.recursive_dls(node)
        self.assertEqual(result.state, self.puzzle.goal_state)

    def test_edge_values_2(self):
        self.puzzle = Puzzle([1, 2, 3, 4, 5, 6, 7, 8, 0])
        node = Node(self.puzzle.initial_state, None, "INIT", 0)
        self.dls = DLS(self.puzzle, 0)
        result = self.dls.recursive_dls(node)
        self.assertEqual(result.state, self.puzzle.goal_state)


class TestRBFS(unittest.TestCase):
    def test_negative(self):
        print("RBFS tests")
        self.puzzle = Puzzle([2, 1, 3, 4, 5, 6, 7, 8, 0])
        node = Node(self.puzzle.initial_state, None, "INIT", 0)
        self.rbfs = RBFS(self.puzzle)
        result = self.rbfs.rbfs(node, 0)
        self.assertEqual(result[0], None)

    def test_positive(self):
        self.puzzle = Puzzle([1, 2, 3, 4, 5, 6, 7, 0, 8])
        node = Node(self.puzzle.initial_state, None, "INIT", 0)
        self.rbfs = RBFS(self.puzzle)
        result = self.rbfs.rbfs(node, float('inf'))
        self.assertEqual(result[0].state, self.puzzle.goal_state)

    def test_edge_values_1(self):
        self.puzzle = Puzzle([1, 2, 6, 7, 5, 4, 0, 8, 3])
        node = Node(self.puzzle.initial_state, None, "INIT", 0)
        self.rbfs = RBFS(self.puzzle)
        result = self.rbfs.rbfs(node, float('inf'))
        self.assertEqual(result[0].state, self.puzzle.goal_state)

    def test_edge_values_2(self):
        self.puzzle = Puzzle([1, 2, 3, 4, 5, 6, 7, 8, 0])
        node = Node(self.puzzle.initial_state, None, "INIT", 0)
        self.rbfs = RBFS(self.puzzle)
        result = self.rbfs.rbfs(node, float('inf'))
        self.assertEqual(result[0].state, self.puzzle.goal_state)


if __name__ == '__main__':
    unittest.main()
