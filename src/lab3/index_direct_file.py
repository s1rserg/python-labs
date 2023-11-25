import math
import os
import random


class IndexDirectFile:
    def __init__(self, num_indexes, index_filename, main_filename, overflow_filename, fill_coefficient):
        self.num_indexes = num_indexes
        self.index_n = index_filename
        self.main_n = main_filename
        self.overflow_n = overflow_filename
        self.fill_coefficient = fill_coefficient
        self.b_size = 10
        self.max_index = 10
        self.empty = "000000None"
        self.lines = []
        self.main_lines = []
        self.overflow_lines = []

    def generate_file(self):
        indexes_per_block = int(self.b_size * self.fill_coefficient)
        empty_spaces_per_block = self.b_size - indexes_per_block
        num_blocks = (self.num_indexes + indexes_per_block - 1) // indexes_per_block
        shuffled_list = list(range(1, self.num_indexes + 1))
        random.shuffle(shuffled_list)

        shuffled_iterator = 0
        with open(self.index_n, 'w') as f:
            for i in range(num_blocks):
                for j in range(indexes_per_block):
                    index = i * indexes_per_block + j + 1
                    if index <= self.num_indexes:
                        f.write(
                            f'{str(index).zfill(self.max_index)},{str(shuffled_list[shuffled_iterator]).zfill(self.max_index)}\n')
                        shuffled_iterator += 1
                    else:
                        f.write(f'{self.empty},{self.empty}\n')
                for _ in range(empty_spaces_per_block):
                    f.write(f'{self.empty},{self.empty}\n')
        with open(self.main_n, 'w') as f:
            for i in range(len(shuffled_list)):
                f.write(f'value{str(shuffled_list.index(i + 1) + 1).zfill(self.max_index)}\n')
        with open(self.overflow_n, 'w') as _:
            pass

    def upload_data(self):
        with open(self.main_n, 'r') as f:
            self.main_lines = [line.strip() for line in f]
        with open(self.index_n, 'r') as f:
            self.lines = [line.strip().split(',') for line in f]
        with open(self.overflow_n, 'r') as f:
            self.overflow_lines = [line.strip().split(',') for line in f]

    def formatted_write(self, filename):
        if filename == self.main_n:
            with open(self.main_n, 'w') as f:
                for line in self.main_lines:
                    f.write(f"{line}\n")
            return
        data = self.lines if filename == self.index_n else self.overflow_lines
        with open(filename, 'w') as f:
            for row in data:
                formatted_row = [str(item).zfill(self.max_index) for item in row]
                f.write(','.join(formatted_row) + '\n')

    def find_block(self, lines, key):
        if key == lines[0] or lines[0] == [self.empty]:
            return 0, 1
        lines = lines[:] + [float('inf')] * (self.b_size + 1)
        max_i = ((len(lines) - (self.b_size + 1)) // self.b_size)
        k = int(math.log(max_i, 2))
        i = 2 ** k
        while True:
            if lines[i * self.b_size] is None or lines[(i + 1) * self.b_size] is None:
                i = i + 1 if i < max_i else i - 1
            else:
                break
        if lines[i * self.b_size] <= key < lines[(i + 1) * self.b_size]:
            return i, 1
        elif lines[i * self.b_size] > key:
            return self.binary_search(lines, i, k, key)
        else:
            l = int(math.log(max_i - 2 ** k + 1, 2))
            return self.binary_search(lines, (max_i + 1 - 2 ** l), l, key)

    def binary_search(self, lines, i, arg, key):
        max_i = ((len(lines) - (self.b_size + 1)) // self.b_size)
        s_iterator = 1
        s = 2 ** (arg - s_iterator)
        comparisons_num = 1
        while True:
            comparisons_num += 1
            while True:
                if lines[i * self.b_size] is None or lines[(i + 1) * self.b_size] is None:
                    i = i + 1 if i < max_i else i - 1
                else:
                    break
            if lines[i * self.b_size] <= key < lines[(i + 1) * self.b_size]:
                return i, comparisons_num
            elif lines[i * self.b_size] > key:
                i -= (s + 1)
            else:
                i += (s + 1)
            i = max(i, 0)
            i = min(i, max_i)
            s_iterator += 1
            if s == 0:
                break
            s = 2 ** (arg - s_iterator)
            if s < 1:
                s = 0
        return i, comparisons_num

    def search(self, key, check=True):
        lines_index = [int(line[0]) if line[0] != self.empty else None for line in self.lines]
        block_index, comparisons_num = self.find_block(lines_index, key)

        block = lines_index[block_index * self.b_size: (block_index + 1) * self.b_size]
        if not check:
            return block_index

        key_in_overflow = False
        if key in block:  # ключ є у індексному файлі
            key_index = block.index(key) + block_index * self.b_size
        elif block.index(None) == self.b_size - 1 and self.lines[(block_index + 1) * self.b_size - 1][1] != self.empty:
            # ключ може бути у області переповнення
            lines_index_overflow = [int(line[0]) if line[0] != self.empty else None for line in self.overflow_lines]
            block_index = int(self.lines[(block_index + 1) * self.b_size - 1][1])
            block = lines_index_overflow[block_index * self.b_size:(block_index + 1) * self.b_size]
            while True:
                if key in block:
                    key_index = block.index(key) + block_index * self.b_size
                    key_in_overflow = True
                    break
                elif self.overflow_lines[(block_index + 1) * self.b_size - 1][1] == self.empty:
                    return None
                else:
                    block_index = int(self.overflow_lines[(block_index + 1) * self.b_size - 1][1])
                    block = lines_index_overflow[block_index * self.b_size: (block_index + 1) * self.b_size]
        else:
            return None

        main_index = int(self.overflow_lines[key_index][1]) - 1 if key_in_overflow else int(
            self.lines[key_index][1]) - 1
        return block_index, key_index, main_index, key_in_overflow, comparisons_num, self.main_lines[main_index]

    def modify(self, key, updated_value):
        indexes = self.search(key)
        if indexes is None:
            return None
        self.main_lines[indexes[2]] = updated_value
        return True

    def remove(self, key):
        indexes = self.search(key)
        if indexes is None:
            return
        block_index, main_index = indexes[0], indexes[2]
        key_in_block_index = indexes[1] - indexes[0] * self.b_size
        lines = self.lines if not indexes[3] else self.overflow_lines
        block = lines[block_index * self.b_size: (block_index + 1) * self.b_size]
        block[key_in_block_index] = [self.empty, self.empty]
        for i in range(key_in_block_index + 1, len(block) - 1):
            if block[i] != [self.empty, self.empty]:
                block[i - 1], block[i] = block[i], block[i - 1]
        lines[block_index * self.b_size:(block_index + 1) * self.b_size] = block
        self.main_lines[main_index] = '00000000Removed'
        return True

    def custom_sort(self, item):
        if item[0] == self.empty:
            return float('inf')
        else:
            return int(item[0])

    def add(self, key, value):
        indexes = self.search(key)
        if indexes is not None:
            return None
        block_index = self.search(key, False)
        block_lines = self.lines[block_index * self.b_size: (block_index + 1) * self.b_size]

        key = str(key).zfill(10)
        main_index = str(len(self.main_lines) + 1).zfill(10)
        self.main_lines.append(value)

        if block_index + 1 == len(self.lines) // self.b_size and (not [self.empty, self.empty] in block_lines or
                                                                  block_lines.index(
                                                                      [self.empty, self.empty]) == self.b_size - 1):
            self.lines += [[key, main_index]]
            self.lines += [[self.empty, self.empty]] * (self.b_size - 1)
            return True
        if (len(self.lines) // self.b_size > block_index + 1 and self.lines[(block_index + 1) * self.b_size][
            0] == self.empty
                and (not [self.empty, self.empty] in block_lines
                     or block_lines.index([self.empty, self.empty]) == self.b_size - 1)):
            self.lines[(block_index + 1) * self.b_size] = [key, main_index]
            return True

        if [self.empty, self.empty] in block_lines:  # є вільне місце у основному блоці
            block_pos = block_lines.index([self.empty, self.empty])
            if block_pos != self.b_size - 1:  # є більш ніж 2 місця у основному блоці
                block_lines[block_pos] = [key, main_index]
                block_lines = sorted(block_lines, key=self.custom_sort)
                self.lines[block_index * self.b_size:(block_index + 1) * self.b_size] = block_lines
            else:  # є лише 1 місце у основному блоці, треба створювати блок для переповнення
                values_block = block_lines[:-1] + [[key, main_index]]
                values_block = sorted(values_block, key=self.custom_sort)
                overflow_value = values_block[-1]
                values_block = values_block[:-1]
                if len(self.overflow_lines) > 0:  # є область переповнення
                    values_block += [[self.empty, str(len(self.overflow_lines) // self.b_size).zfill(self.max_index)]]
                    self.overflow_lines += [overflow_value]
                else:  # немає області переповнення
                    values_block += [[self.empty, '0000000000']]
                    self.overflow_lines = [overflow_value]

                self.overflow_lines += [[self.empty, self.empty]] * (self.b_size - 1)
                self.lines[block_index * self.b_size:(block_index + 1) * self.b_size] = values_block

        else:  # немає вільного місця в блоці -> вже існує відповідний блок у області переповнення
            index_block_overflow = int(block_lines[-1][1])
            block_overflow = self.overflow_lines[index_block_overflow *
                                                 self.b_size:(index_block_overflow + 1) * self.b_size]
            all_indexes = []
            all_blocks = block_lines[:-1] + [[key, main_index]]
            while True:
                if [self.empty, self.empty] in block_overflow:  # є пусте місце в блоці
                    break
                else:
                    all_indexes.append(index_block_overflow)
                    all_blocks += block_overflow[:-1]
                    index_block_overflow = int(block_overflow[-1][1])
                    block_overflow = self.overflow_lines[index_block_overflow *
                                                         self.b_size:(index_block_overflow + 1) * self.b_size]
            empty_index = block_overflow.index([self.empty, self.empty])
            all_indexes.append(index_block_overflow)
            all_blocks += block_overflow
            all_blocks = sorted(all_blocks, key=self.custom_sort)
            self.lines[block_index * self.b_size:(block_index + 1) * self.b_size - 1] = all_blocks[:self.b_size - 1]
            all_blocks = all_blocks[self.b_size - 1:]
            if empty_index == self.b_size - 1:  # якщо є тільки одне вільне місце
                self.overflow_lines[index_block_overflow * self.b_size + (self.b_size - 1)] = \
                    [self.empty, str(len(self.overflow_lines) // self.b_size).zfill(10)]
                self.overflow_lines += [all_blocks[-2]]  # all_blocks[-1] = None
                self.overflow_lines += [[self.empty, self.empty]] * (self.b_size - 1)
            for i, index in enumerate(all_indexes):
                self.overflow_lines[index * self.b_size:(index + 1) * self.b_size - 1] = \
                    all_blocks[i * (self.b_size - 1):(i + 1) * (self.b_size - 1)]
        return True

    def validate(self):
        if not os.path.exists(self.index_n):
            return False, "Index file doesn't exist"
        if not os.path.exists(self.main_n):
            return False, "Main file doesn't exist"
        if not os.path.exists(self.overflow_n):
            return False, "Overflow file doesn't exist"
        with open(self.main_n, 'r') as f:
            for line in f:
                if len(line.rstrip('\n')) != self.max_index + 5:
                    return False, "Main file is corrupted"
        with open(self.index_n, 'r') as f:
            for line in f:
                if len(line.rstrip('\n')) != 2 * self.max_index + 1:
                    return False, "Index file is corrupted"
        with open(self.overflow_n, 'r') as f:
            for line in f:
                if len(line.rstrip('\n')) != 2 * self.max_index + 1:
                    return False, "Overflow file is corrupted"
        return True, "Success"
