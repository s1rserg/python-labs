import random


class Graph:
    def __init__(self, size, vertex_lo, vertex_hi, length_lo, length_hi):
        self.adj_matrix = [[0] * size for _ in range(size)]
        self.size = size
        self.vertex_lo = vertex_lo
        self.vertex_hi = vertex_hi
        self.length_lo = length_lo
        self.length_hi = length_hi
        self.generate()

    def generate(self):
        for row_index in range(self.size - 1):
            taken = sum(1 for value in self.adj_matrix[row_index][:row_index] if value != 0)
            bound = random.randint(self.vertex_lo, self.vertex_hi) - taken
            for i in range(bound):
                pos_value = random.randint(row_index + 1, self.size - 1)
                taken_y = sum(self.adj_matrix[pos_value][:row_index])
                if taken_y >= self.vertex_hi:
                    continue
                self.adj_matrix[row_index][pos_value] = 1
                self.adj_matrix[pos_value][row_index] = 1

        for row_index in range(self.size):
            for col_index in range(row_index):
                if self.adj_matrix[row_index][col_index]:
                    length_value = random.randint(self.length_lo, self.length_hi)
                    self.adj_matrix[row_index][col_index] = self.adj_matrix[col_index][row_index] = length_value
        self.is_valid_matrix()

    def is_valid_matrix(self):
        for i in range(self.size):
            non_zero_count = sum(1 for value in self.adj_matrix[i] if value != 0)
            if non_zero_count < self.vertex_lo or non_zero_count > self.vertex_hi:
                self.adj_matrix = [[0] * self.size for _ in range(self.size)]
                self.generate()

    def print_matrix(self):
        for row in self.adj_matrix:
            print(', '.join(map(str, row)))
