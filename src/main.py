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


def quicksort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        less = [x for x in arr[1:] if x <= pivot]
        greater = [x for x in arr[1:] if x > pivot]
        return quicksort(less) + [pivot] + quicksort(greater)


def merge_series(input, output):
    files = [open(input_file, 'r') for input_file in input]
    input_files = [mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) for f, input_file in zip(files, input) if
                   os.stat(input_file).st_size != 0]
    output_files = [open(output_file, 'w') for output_file in output]

    buffers = [None] * len(input_files)

    while True:
        series = []
        for i, input_file in enumerate(input_files):
            file_series = []
            line = buffers[i] if buffers[i] is not None else input_file.readline()
            buffers[i] = None
            while line:
                num = int(line)
                if not file_series or num >= file_series[-1]:
                    file_series.append(num)
                    line = input_file.readline()
                else:
                    buffers[i] = line
                    break
            series.extend(file_series)

        if not series and all(not buffer for buffer in buffers):
            break

        series = quicksort(series)
        output_file = output_files[0]
        for number in series:
            output_file.write(str(number) + '\n')
        series.clear()

        output_files = output_files[1:] + [output_files[0]]

    for file in input_files + output_files:
        file.close()

    if not(os.stat(output[-1]).st_size == 0 and os.stat(output[-2]).st_size == 0):
        print("Run completed!")
        merge_series(output, input)


def main():
    file_size = 10 * 1024 ** 2
    input_file = "a1.txt"
    output_files_1 = ["b1.txt", "b2.txt", "b3.txt"]
    output_files_2 = ["c1.txt", "c2.txt", "c3.txt"]
    generate(input_file, file_size)
    clear_files(output_files_1)
    split_series(input_file, output_files_1)
    merge_series(output_files_1, output_files_2)
    print("Successfully sorted!")


main()
