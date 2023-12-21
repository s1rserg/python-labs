import unittest
from bee_colony import BeesAlgorithm, Graph
# конкретну поведінку функцій, які використовують випадкові числа, наприклад функцію локального пошуку передбачити неможливо,
# тому тестую лише те, чиї результати можна з чимось порівнювати

class TestBeeAlgorithm(unittest.TestCase):

    def test_calculate_fitness_positive(self):
        print("calculate fitness tests")
        graph = Graph(5, 1, 5, 1, 10)
        graph.adj_matrix = [
            [0, 0, 1, 0, 9],
            [0, 0, 5, 0, 6],
            [1, 5, 0, 7, 0],
            [0, 0, 7, 0, 0],
            [9, 6, 0, 0, 0]
        ]
        ba = BeesAlgorithm(5, 3, graph, 0, 4, 10)
        path = [[0, 1, 2, 3, 4], 0]
        ba.calculate_fitness(path)
        self.assertEqual(path[1], 12)


    def test_calculate_fitness_negative(self):
        graph = Graph(5, 1, 5, 1, 10)
        graph.adj_matrix = [
            [0, 0, 1, 0, 9],
            [0, 0, 5, 0, 6],
            [1, 5, 0, 7, 0],
            [0, 0, 7, 0, 0],
            [9, 6, 0, 0, 0]
        ]
        ba = BeesAlgorithm(5, 3, graph, 0, 4, 10)
        path = [[0], 0]
        ba.calculate_fitness(path)
        self.assertEqual(path[1], 0)

    def test_calculate_fitness_edge(self):
        graph = Graph(5, 1, 5, 1, 10)
        graph.adj_matrix = [
            [0, 0, 1, 0, 9],
            [0, 0, 5, 0, 6],
            [1, 5, 0, 7, 0],
            [0, 0, 7, 0, 0],
            [9, 6, 0, 0, 0]
        ]
        ba = BeesAlgorithm(5, 3, graph, 0, 4, 10)
        path = [[0, 0], 0]
        ba.calculate_fitness(path)
        self.assertEqual(path[1], 0)

class TestTaskGraph(unittest.TestCase):

    def test_generate_positive(self):
        print("graph generator tests")
        graph = Graph(5, 1, 5, 1, 10)
        graph.generate()
        counter = 0
        for i in range(graph.size):
            non_zero_count = sum(1 for value in graph.adj_matrix[i] if value != 0)
            if non_zero_count < graph.vertex_lo - 1 or non_zero_count > graph.vertex_hi + 1:
                counter += 1
        self.assertEqual(counter, 0)

    def test_generate_edge_values(self):
        graph = Graph(5, 1, 5, 1, 10)
        graph.generate()
        counter = 0
        for i in range(graph.size):
            non_zero_count = sum(1 for value in graph.adj_matrix[i] if value != 0)
            if non_zero_count < graph.vertex_lo - 1 or non_zero_count > graph.vertex_hi + 1:
                counter += 1
        self.assertEqual(counter, 0)

if __name__ == '__main__':
    unittest.main()
