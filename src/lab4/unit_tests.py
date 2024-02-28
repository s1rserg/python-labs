import unittest
from knapsack import *


class TestKnapsack(unittest.TestCase):

    def test_calculate_value(self):
        knapsack = Knapsack(3, 1, (1, 5), (1, 10), 6, 0.05, 1000)
        knapsack.items = [(2, 3), (1, 5), (4, 8)]

        # Positive case
        self.assertEqual(knapsack.calculate_value([1, 0, 1]), 11)

        # Edge case
        self.assertEqual(knapsack.calculate_value([0, 0, 0]), 0)

        # Negative case
        self.assertEqual(knapsack.calculate_value([1, 1, 1]), 0)
        print("calculate_value tests passed.")

    def test_record_counter(self):
        knapsack = Knapsack(3, 2, (1, 5), (1, 10), 5, 0.05, 1000)
        knapsack.items = [(2, 3), (1, 5), (4, 8)]
        knapsack.population = [[1, 0, 1], [0, 1, 0]]

        # Positive case
        knapsack.record_counter()
        self.assertEqual(knapsack.record, 5)

        # Negative case
        knapsack.population = [[0, 0, 0], [0, 0, 0]]
        knapsack.record_counter()
        self.assertEqual(knapsack.record, 0)
        print("record_counter tests passed.")

    def test_crossover(self):
        knapsack = Knapsack(4, 1, (1, 5), (1, 10), 10, 0.05, 1000)
        parent1 = [1, 0, 1, 0]
        parent2 = [0, 1, 0, 1]

        # Positive case
        child1, child2 = knapsack.crossover(parent1, parent2)
        self.assertEqual(len(child1), 4)
        self.assertEqual(len(child2), 4)
        self.assertEqual(set(child1 + child2), {0, 1})
        print("crossover tests passed.")

    def test_mutation(self):
        knapsack = Knapsack(3, 1, (1, 5), (1, 10), 5, 0.5, 1000)
        knapsack.items = [(2, 3), (1, 5), (4, 8)]
        child = [1, 0, 1]

        # Positive case
        mutated_child = knapsack.mutation([child])[0]
        self.assertEqual(set(mutated_child), {0, 1})

        # Negative case
        knapsack.mutation([])
        print("mutation tests passed.")

    def test_local_improvement(self):
        knapsack = Knapsack(3, 1, (1, 5), (1, 10), 10, 0.05, 1000)
        knapsack.items = [(2, 3), (1, 5), (4, 8)]
        child = [1, 0, 1]

        # Positive case
        improved_child = knapsack.local_improvement([child])[0]
        self.assertEqual(set(improved_child), {0, 1})

        # Negative case
        knapsack.local_improvement([])
        print("local_improvement tests passed.")


if __name__ == '__main__':
    unittest.main()
