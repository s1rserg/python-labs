import random


class Knapsack:
    def __init__(self, num_items, population_size, weight_bounds, value_bounds, max_weight, mutation_probability, iterations):
        self.num_items = num_items
        self.weight_bounds = weight_bounds
        self.value_bounds = value_bounds
        self.population_size = population_size
        self.max_weight = max_weight
        self.mutation_probability = mutation_probability
        self.items = []
        self.population = []
        self.record = 0
        self.record_chromosome = []
        self.iterations = iterations

    def generate_initial_population(self, difficulty_factor=2.3):
        self.population = [
            [random.choices([0, 1], weights=[difficulty_factor, 1], k=1)[0]
             for _ in range(self.num_items)]
            for _ in range(self.population_size)
        ]

    def generate_items_data(self):
        self.items = [[random.randint(*self.weight_bounds), random.randint(*self.value_bounds)]
                      for _ in range(self.num_items)]

    def calculate_value(self, chromosome):
        total_weight = 0
        total_value = 0
        for i in range(len(chromosome)):
            if chromosome[i] == 1:
                total_weight += self.items[i][0]
                total_value += self.items[i][1]
        if total_weight > self.max_weight:
            return 0
        else:
            return total_value

    def record_counter(self):
        max_chromosome = max(self.population, key=lambda chromosome: self.calculate_value(chromosome))
        self.record = self.calculate_value(max_chromosome)
        self.record_chromosome = max_chromosome

    def select_parents(self):
        # пропорційна селекція
        values = []
        for chromosome in self.population:
            values.append(self.calculate_value(chromosome))

        values_sum = sum(values)
        if values_sum:
            proportional_values = [float(i)/values_sum for i in values]
            while True:
                parent1 = random.choices(self.population, weights=proportional_values, k=1)[0]
                parent1_index = self.population.index(parent1)
                parent2 = random.choices(self.population, weights=proportional_values, k=1)[0]
                parent2_index = self.population.index(parent2)
                if parent1_index == parent2_index:
                    while True:
                        parent2_index = random.randint(0, self.population_size - 1)
                        if parent2_index != parent1_index:
                            break
                    parent2 = self.population[parent2_index]
                    break

        else:
            while True:
                parent1_index, parent2_index = (random.randint(0, self.population_size - 1),
                                                random.randint(0, self.population_size - 1))
                if parent1_index != parent2_index:
                    break
            parent1 = self.population[parent1_index]
            parent2 = self.population[parent2_index]
        return parent1, parent2

    def crossover(self, parent1, parent2):
        # триточковий оператор схрещування 25%
        size = self.num_items // 4
        parent1 = [parent1[i:i+size] for i in range(0, self.num_items, size)]
        parent2 = [parent2[i:i+size] for i in range(0, self.num_items, size)]
        child1 = parent1[0] + parent2[1] + parent1[2] + parent2[3]
        child2 = parent2[0] + parent1[1] + parent2[2] + parent1[3]
        return child1, child2

    def mutation(self, children):
        children_values = [self.calculate_value(child) for child in children]
        for i in range(len(children)):
            mutation_num = random.random()
            if mutation_num < self.mutation_probability:
                mutation_index = random.randint(0, self.num_items - 1)
                children[i][mutation_index] = int(not children[i][mutation_index])
                if children_values[i] and not self.calculate_value(children[i]):
                    # якщо мутація зробила хромосому мертвою
                    children[i][mutation_index] = int(not children[i][mutation_index])
        return children

    def local_improvement(self, children):
        # серед допустимих шукаємо предмет з найменшою вагою і додаємо його
        children_values = [self.calculate_value(child) for child in children]
        for i in range(len(children)):
            available_items_indexes = [index for index, value in enumerate(children[i]) if value == 1]
            available_items = [self.items[index] for index in available_items_indexes]
            if not available_items:
                continue
            min_weight_item = min(available_items, key=lambda x: x[0])
            min_weight_item_index = self.items.index(min_weight_item)
            children[i][min_weight_item_index] = 1
            if children_values[i] and not self.calculate_value(children[i]):
                # якщо покращення зробило хромосому мертвою
                children[i][min_weight_item_index] = 0
        return children

    def iteration(self):
        parents = self.select_parents()
        children = self.crossover(parents[0], parents[1])
        children = self.mutation(children)
        children = self.local_improvement(children)

        population_values = [self.calculate_value(chromosome) for chromosome in self.population]
        for i, child in enumerate(children):
            min_population_element = min(enumerate(population_values), key=lambda x: x[1])
            child_value = self.calculate_value(child)
            if child_value and min(child_value, min_population_element[1]) == min_population_element[1]:
                self.population[min_population_element[0]] = child
        self.record_counter()

    def genetic_algorithm(self):
        i_values = []
        record_values = []
        for i in range(self.iterations + 1):
            self.iteration()
            if i % 20 == 0:
                i_values.append(i)
                record_values.append(self.record)
        return i_values, record_values

    def result(self):
        print("Items [Weight, Value]: ", self.items)
        total_weight = 0
        num_of_items = 0
        for i in range(len(self.record_chromosome)):
            if self.record_chromosome[i] == 1:
                total_weight += self.items[i][0]
                num_of_items += 1
        if total_weight > self.max_weight:
            print("Solution was not found")
            return
        print("Solution: ", self.record_chromosome)
        print("Knapsack value: ", self.record)
        print("Knapsack weight: ", total_weight)
        print("Num of items in knapsack: ", num_of_items)
