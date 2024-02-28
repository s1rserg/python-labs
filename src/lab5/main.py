from bee_colony import *
from helpers import *
VERTEX_AMOUNT = 300
LENGTH_LO = 5
LENGTH_HI = 150
VERTEX_LO = 1
VERTEX_HI = 10
ITERATIONS_NUM = 30


def main():
    while True:
        onlookers = input("Amount of onlookers: ")
        if validate_positive_integer(onlookers):
            break
    onlookers = int(onlookers)
    while True:
        employed = input("Amount of employed: ")
        if validate_positive_integer(employed):
            break
    employed = int(employed)
    graph = Graph(VERTEX_AMOUNT, VERTEX_LO, VERTEX_HI, LENGTH_LO, LENGTH_HI)
    ba = BeesAlgorithm(onlookers, employed, graph, 0, 299, ITERATIONS_NUM)
    ba.solve()
    best_path = ba.get_best_path()
    print("PATH (vertices):",  '->'.join(map(str, best_path[0][0])))
    print(f"total length: {best_path[0][1]} | PATH (weights):", '+'.join(map(str, best_path[1])))


if __name__ == "__main__":
    main()
