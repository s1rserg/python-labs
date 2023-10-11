import unittest
import os
import random

import series_merger
import mod_series_merger
import series_splitter
import chunk_sorter


class TestSplitSeries(unittest.TestCase):
    def setUp(self):
        self.input_file = 'input.txt'
        self.output_files = ['output1.txt', 'output2.txt']
        self.series_splitter = series_splitter.SeriesSplitter(self.input_file, self.output_files)

    def tearDown(self):
        files = [self.input_file] + self.output_files
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    def test_positive(self):
        print("SplitSeries tests")
        arr = [8, 23, 1, 6, 33, 5, 65, 29, 31, 27, 48]
        for i in range(0, len(arr)):
            arr[i] = str(arr[i])
        with open(self.input_file, 'w') as f:
            f.write('\n'.join(arr))

        self.series_splitter.split_series()

        with open(self.output_files[0], 'r') as f:
            data = list(map(int, f.read().split()))
            self.assertEqual(data, [8, 23, 5, 65, 27, 48])
        with open(self.output_files[1], 'r') as f:
            data = list(map(int, f.read().split()))
            self.assertEqual(data, [1, 6, 33, 29, 31])

    def test_negative(self):
        with open(self.input_file, 'w') as f:
            f.write('a\nb\nc\n')

        with self.assertRaises(ValueError):
            self.series_splitter.split_series()

    def test_edge(self):
        with open(self.input_file, 'w') as _:
            pass

        self.series_splitter.split_series()

        for output_file in self.output_files:
            with open(output_file, 'r') as f:
                data = f.read()
                self.assertEqual(data, '')


class TestMergeSeries(unittest.TestCase):
    def setUp(self):
        self.input_files = ['input1.txt', 'input2.txt']
        self.output_files = ['output1.txt', 'output2.txt']
        self.size = 1024
        self.series_merger = series_merger.SeriesMerger(self.input_files, self.output_files, self.size)

    def tearDown(self):
        for file in self.input_files + self.output_files:
            if os.path.exists(file):
                os.remove(file)

    def test_positive(self):
        print("MergeSeries tests")
        with open(self.input_files[0], 'w') as f:
            f.write('\n'.join(map(str, random.sample(range(1000), 500))))
        with open(self.input_files[1], 'w') as f:
            f.write('\n'.join(map(str, random.sample(range(1000), 500))))

        self.series_merger.merge_series()

        with open(self.output_files[0], 'r') as f:
            data = list(map(int, f.read().split()))
            self.assertEqual(data, sorted(data))

    def test_negative(self):
        with open(self.input_files[0], 'w') as f:
            f.write('a\nb\nc\n')
        with open(self.input_files[1], 'w') as f:
            f.write('a\nb\nc\n')

        with self.assertRaises(ValueError):
            self.series_merger.merge_series()

    def test_edge(self):
        with open(self.input_files[0], 'w') as _:
            with open(self.input_files[1], 'w') as _:
                pass
        self.series_merger.merge_series()
        with open(self.output_files[0], 'r') as f:
            data = f.read()
            self.assertEqual(data, '')


class TestChunkSorter(unittest.TestCase):
    def setUp(self):
        self.input_file = 'input.txt'
        self.output_files = ['output1.txt', 'output2.txt']
        self.chunk_sorter = chunk_sorter.ChunkSorter(self.input_file, self.output_files)

    def tearDown(self):
        files = [self.input_file] + self.output_files
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    def test_positive(self):
        print("ChunkSorter tests")
        with open(self.input_file, 'w') as f:
            f.write('\n'.join(map(str, range(10 ** 6))))
        with open(self.output_files[0], 'w') as _:
            with open(self.output_files[1], 'w') as _:
                pass
        self.chunk_sorter.sort_chunks()

        for output_file in self.output_files:
            self.assertGreater(os.path.getsize(output_file), 0)

    def test_negative(self):
        with open(self.input_file, 'w') as f:
            f.write('a\nb\nc\n')

        with self.assertRaises(ValueError):
            self.chunk_sorter.sort_chunks()

    def test_edge(self):
        with open(self.input_file, 'w') as f:
            f.write('1')

        self.chunk_sorter.sort_chunks()

        with open(self.output_files[0], 'r') as f:
            data = int(f.read())
        self.assertEqual(data, 1)


class TestModMergeSeries(unittest.TestCase):
    def setUp(self):
        self.input_files = ['input1.txt', 'input2.txt']
        self.output_files = ['output1.txt', 'output2.txt']
        self.size = 1024
        self.series_merger = mod_series_merger.SeriesMerger(self.input_files, self.output_files, self.size)

    def tearDown(self):
        for file in self.input_files + self.output_files:
            if os.path.exists(file):
                os.remove(file)

    def test_positive(self):
        print("ModMergeSeries tests")
        with open(self.input_files[0], 'w') as f:
            f.write('\n'.join(map(str, random.sample(range(1000), 500))))
        with open(self.input_files[1], 'w') as f:
            f.write('\n'.join(map(str, random.sample(range(1000), 500))))

        self.series_merger.merge_series()

        with open(self.output_files[0], 'r') as f:
            data = list(map(int, f.read().split()))
            self.assertEqual(data, sorted(data))

    def test_negative(self):
        with open(self.input_files[0], 'w') as f:
            f.write('a\nb\nc\n')
        with open(self.input_files[1], 'w') as f:
            f.write('a\nb\nc\n')

        with self.assertRaises(ValueError):
            self.series_merger.merge_series()

    def test_edge(self):
        with open(self.input_files[0], 'w') as _:
            with open(self.input_files[1], 'w') as _:
                pass
        self.series_merger.merge_series()
        with open(self.output_files[0], 'r') as f:
            data = f.read()
            self.assertEqual(data, '')


if __name__ == '__main__':
    unittest.main()
