from graph import *
FAIL_SEARCH_COUNT = 10


class BeesAlgorithm:
    def __init__(self, onlookers, employed, graph, start_vertex, end_vertex, iterations_num):
        self.onlookers_num = onlookers
        self.employed_num = employed
        self.graph = graph
        self.size = self.graph.size
        self.path_counters = [[None, 0] for _ in range(self.employed_num)]  # зберігається к-сть невдалих пошуків
        self.paths = [[[], 0] for _ in range(self.employed_num)]
        self.record_fitness = 0
        self.start_vertex = start_vertex
        self.end_vertex = end_vertex
        self.record_fitness = 0
        self.iterations_num = iterations_num
        self.records = []

    def calculate_fitness(self, path):
        vertices = path[0]
        path[1] = sum(self.graph.adj_matrix[vertices[i]][vertices[i + 1]] for i in range(len(vertices) - 1))

    def local_search(self, start_vertex, end_vertex):
        path = [start_vertex]
        current_vertex = start_vertex
        steps_taken = 0

        while current_vertex != end_vertex:
            possible_next_vertices = [
                [neighbor, self.graph.adj_matrix[current_vertex][neighbor]]
                for neighbor in range(self.graph.size)
                if self.graph.adj_matrix[current_vertex][neighbor]
            ]

            current_vertex = roulette_wheel_choice(possible_next_vertices)
            path.append(current_vertex)
            steps_taken += 1

            if steps_taken > self.size - 1:  # шлях більше кількості вершин
                return [-1]

        return path

    def solve(self):
        self.initialize_sources()
        print(f"i = 0 | Init path = {'->'.join(map(str, self.paths[0][0]))}, its length = {self.paths[0][1]}")

        for i in range(self.iterations_num):
            self.records.append(self.paths[self.record_fitness][1])
            self.send_employed()
            self.record_fitness = min(range(self.employed_num), key=lambda x: self.paths[x][1])
            self.send_onlookers()
            print(f"i = {i+1} | Best path = {'->'.join(map(str, self.paths[self.record_fitness][0]))}, its length = {self.paths[self.record_fitness][1]}")

    def send_employed(self):
        for i in range(self.employed_num):
            pivot = random.randint(0, len(self.paths[i][0]) - 1)
            old_part_path = self.paths[i][0][:pivot]
            new_part_path = self.local_search(self.paths[i][0][pivot], self.paths[i][0][-1])

            if new_part_path[0] == -1:  # пошук в околицях не вдався
                continue

            new_path = [old_part_path + new_part_path, 0]
            self.calculate_fitness(new_path)

            if new_path[1] < self.paths[i][1]:  # новий шлях краще старого
                self.paths[i] = new_path

            if self.path_counters[i][1] > FAIL_SEARCH_COUNT and self.record_fitness != i:
                new_path = None
                while new_path is None or new_path[0][0] == -1:
                    new_path = [self.local_search(self.start_vertex, self.end_vertex), 0]

                self.calculate_fitness(new_path)
                self.paths[i] = new_path
                self.path_counters[i] = [None, 0]

    def send_onlookers(self):
        proportional_values = [[i, 1 / self.paths[i][1]] for i in range(self.employed_num)]
        for _ in range(self.onlookers_num):
            chosen_path = roulette_wheel_choice(proportional_values)
            pivot = random.randint(0, len(self.paths[chosen_path][0]) - 1)
            old_part_path = self.paths[chosen_path][0][:pivot]
            new_part_path = self.local_search(self.paths[chosen_path][0][pivot], self.paths[chosen_path][0][-1])

            if new_part_path[0] == -1:  # пошук в околицях не вдався
                self.path_counters[chosen_path] = [None, self.path_counters[chosen_path][1] + 1]
                continue

            new_path = [old_part_path + new_part_path, 0]
            self.calculate_fitness(new_path)

            if new_path[1] < self.paths[chosen_path][1]:  # новий шлях краще старого
                self.paths[chosen_path] = new_path
                self.path_counters[chosen_path] = [None, 0]

    def initialize_sources(self):
        init_path = None
        while init_path is None or init_path[0][0] == -1:
            init_path = [self.local_search(self.start_vertex, self.end_vertex), 0]
            self.calculate_fitness(init_path)

        for i in range(self.employed_num):
            self.paths[i] = init_path

    def get_best_path(self):
        weights = []
        for i in range(len(self.paths[self.record_fitness][0]) - 1):
            cur_element = self.paths[self.record_fitness][0][i]
            next_element = self.paths[self.record_fitness][0][i+1]
            weights.append(self.graph.adj_matrix[cur_element][next_element])
        return self.paths[self.record_fitness], weights


def roulette_wheel_choice(values):
    weights = [value[1] for value in values]
    chosen_value = random.choices(values, weights=weights, k=1)[0]
    return chosen_value[0]

