import time
from number_generator import NumberGenerator
from series_splitter import SeriesSplitter
from series_merger import SeriesMerger
import validators


def main():
    while True:
        file_size = input("Enter file size (megabytes): ")
        if not validators.validate_positive_integer(file_size):
            print("The input is not a valid positive integer. Please try again.")
        else:
            file_size = int(file_size) * 1024 ** 2
            break
    input_file = "a.txt"
    output_files_1 = ["b1.txt", "b2.txt", "b3.txt"]
    output_files_2 = ["c1.txt", "c2.txt", "c3.txt"]

    number_generator = NumberGenerator(input_file, file_size)
    number_generator.generate()  # генерація чисел

    validators.clear_files(output_files_1)  # очистка допоміжних файлів
    series_splitter = SeriesSplitter(input_file, output_files_1)
    series_merger = SeriesMerger(output_files_1, output_files_2, file_size)
    start_time = time.time()
    series_splitter.split_series()  # поділ на cерії
    print("Series are split")
    series_merger.merge_series()  # сортування
    end_time = time.time()
    print(f"The sorting took {end_time - start_time} seconds.")


if __name__ == "__main__":
    main()
