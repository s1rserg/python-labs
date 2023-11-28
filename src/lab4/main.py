from knapsack import *
from helpers import *
import sys


def main():
    is_graph = False
    if len(sys.argv) > 1:
        if sys.argv[1] == 'gr':
            is_graph = True
        elif sys.argv[1] == 'ngr':
            is_graph = False
        else:
            print("Unexpected parameter")
            return
    if len(sys.argv) > 2:
        try:
            file_data = read_and_parse_file(sys.argv[2])
        except FileNotFoundError as e:
            print(f"Error: {e}")
            return
        except ValueError as e:
            print(f"Error: {e}")
            return
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return
        knapsack = Knapsack(len(file_data), 100, (0, 0), (0, 0), 250, 0.05, 1000)
        knapsack.items = file_data
    else:
        knapsack = Knapsack(100, 100, (1, 25), (2, 30), 250, 0.05, 1000)
        knapsack.generate_items_data()
    knapsack.generate_initial_population()
    knapsack.record_counter()
    i_values, record_values = knapsack.genetic_algorithm()
    if is_graph:
        print("Число ітерацій Значення цільової функції")
        for i in range(len(i_values)):
            print(i_values[i], record_values[i])
        graph(i_values, record_values)
    knapsack.result()


if __name__ == "__main__":
    main()
