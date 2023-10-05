import os
import random
import mmap


def generate(filename, size):
    numbers_per_chunk = 100000
    chunk = ''
    with open(filename, 'w') as f:
        while f.tell() < size:
            chunk += '\n'.join(str(random.randint(1, 1000)) for _ in range(numbers_per_chunk)) + '\n'
            f.write(chunk)
            chunk = ''
    print("Random numbers generated!")


def split_series(input_file, output_files):
    current_series = 0
    last_num = None

    with open(output_files[0], 'w') as out1, open(output_files[1], 'w') as out2, open(output_files[2], 'w') as out3:
        outputs = [out1, out2, out3]

        with open(input_file, 'r') as f:
            for line in f:
                num = int(line.strip())
                if last_num is not None and num < last_num:
                    current_series = (current_series + 1) % 3
                outputs[current_series].write(f"{num}\n")
                last_num = num


def clear_files(files):
    for file in files:
        try:
            with open(file, 'w'):
                pass
        except FileNotFoundError:
            print(f"The file '{file}' does not exist.")
        except Exception as e:
            print(f"An error occurred while clearing '{file}': {str(e)}")


def merge_series(input_files, output_files):
    files = [open(input_file, 'r') for input_file in input_files]
    inputs = [mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) for f, input_file in zip(files, input_files) if
              os.stat(input_file).st_size != 0]
    outputs = [open(output_file, 'w') for output_file in output_files]

    num_of_files = len(inputs)
    values = [None] * num_of_files
    last_values = [None] * num_of_files
    series_ends = [False] * num_of_files
    buffer = [None] * num_of_files
    while True:
        if num_of_files == 0:
            break
        for i in range(num_of_files):
            if values[i] is None and not series_ends[i]:
                if buffer[i]:
                    line = str(buffer[i])
                    buffer[i] = None
                else:
                    line = inputs[i].readline()
                if not line.strip():
                    num_of_files -= 1
                    inputs[i].close()
                    del inputs[i]
                    del values[i]
                    del last_values[i]
                    del series_ends[i]
                    break
                else:
                    values[i] = int(line)
                    if last_values[i] is not None and values[i] < last_values[i]:
                        series_ends[i] = True
                        buffer[i] = values[i]
                        values[i] = None
                    else:
                        last_values[i] = values[i]
        if all(series_ends):
            values = [None] * num_of_files
            last_values = [None] * num_of_files
            series_ends = [False] * num_of_files
            outputs = outputs[1:] + [outputs[0]]
        if any(element is not None for element in values):
            min_value = min(v for v in values if v is not None)
            min_index = values.index(min_value)
            outputs[0].write(str(min_value) + '\n')
            values[min_index] = None

    for file in inputs + outputs:
        file.close()

    if not (os.stat(output_files[-1]).st_size == 0 and os.stat(output_files[-2]).st_size == 0):
        print("Run completed!")
        merge_series(output_files, input_files)


def main():
    file_size = 10 * 1024 ** 2
    input_file = "a2.txt"
    output_files_1 = ["b1.txt", "b2.txt", "b3.txt"]
    output_files_2 = ["c1.txt", "c2.txt", "c3.txt"]
    generate(input_file, file_size)
    clear_files(output_files_1)
    split_series(input_file, output_files_1)
    merge_series(output_files_1, output_files_2)
    print("Successfully sorted!")


main()
