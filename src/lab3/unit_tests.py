import unittest
from index_direct_file import *

index_values = [
    "0000000001,0000000001",
    "0000000002,0000000002",
    "0000000003,0000000003",
    "0000000004,0000000004",
    "0000000005,0000000005",
    "0000000006,0000000006",
    "0000000007,0000000007",
    "0000000008,0000000008",
    "0000000009,0000000009",
    "000000None,0000000000"]

overflow_values = [
    "0000000010,0000000010",
    "000000None,000000None",
    "000000None,000000None",
    "000000None,000000None",
    "000000None,000000None",
    "000000None,000000None",
    "000000None,000000None",
    "000000None,000000None",
    "000000None,000000None",
    "000000None,000000None",
]

main_values = [
    "value0000000001",
    "value0000000002",
    "value0000000003",
    "value0000000004",
    "value0000000005",
    "value0000000006",
    "value0000000007",
    "value0000000008",
    "value0000000009",
    "value0000000010",
]
index_file = 'test.txt'
main_file = 'test_main.txt'
overflow_file = 'overflow.txt'

def write_into_files():
    with open(index_file, 'w') as f:
        for line in index_values:
            f.write(line + "\n")
    with open(overflow_file, 'w') as f:
        for line in overflow_values:
            f.write(line + "\n")
    with open(main_file, 'w') as f:
        for line in main_values:
            f.write(line + "\n")


class TestSearch(unittest.TestCase):
    def setUp(self):
        write_into_files()
        self.index_direct_file = IndexDirectFile(10, index_file, main_file, overflow_file, 0.6)
        self.index_direct_file.upload_data()

    def test_negative(self):
        print("Search tests")
        result = self.index_direct_file.search(11)
        self.assertEqual(result, None)

    def test_positive(self):
        result = self.index_direct_file.search(1)
        self.assertEqual(result[0], 0)
        self.assertEqual(result[-3], False)

    def test_edge_values(self):
        result = self.index_direct_file.search(10)
        self.assertEqual(result[0], 0)
        self.assertEqual(result[-3], True)


class TestModify(unittest.TestCase):
    def setUp(self):
        write_into_files()
        self.index_direct_file = IndexDirectFile(10, index_file, main_file, overflow_file, 0.6)
        self.index_direct_file.upload_data()

    def test_negative(self):
        print("Modify tests")
        result = self.index_direct_file.modify(15, "gsg")
        self.assertEqual(result, None)

    def test_positive(self):
        self.index_direct_file.modify(1, 'gsg')
        self.assertEqual(self.index_direct_file.main_lines[0], 'gsg')

    def test_edge_values(self):
        self.index_direct_file.modify(10, 'gsg')
        self.assertEqual(self.index_direct_file.main_lines[9], 'gsg')


class TestRemove(unittest.TestCase):
    def setUp(self):
        write_into_files()
        self.index_direct_file = IndexDirectFile(10, index_file, main_file, overflow_file, 0.6)
        self.index_direct_file.upload_data()

    def test_negative(self):
        print("Remove tests")
        result = self.index_direct_file.remove(15)
        self.assertEqual(result, None)

    def test_positive(self):
        self.index_direct_file.remove(1)
        self.assertEqual(self.index_direct_file.main_lines[0], '00000000Removed')
        self.assertEqual(self.index_direct_file.lines[0], ['0000000002', '0000000002'])

    def test_edge_values(self):
        self.index_direct_file.remove(10)
        self.assertEqual(self.index_direct_file.main_lines[9], '00000000Removed')
        self.assertEqual(self.index_direct_file.overflow_lines[0], ["000000None", "000000None"])


class TestAdd(unittest.TestCase):
    def setUp(self):
        write_into_files()
        self.index_direct_file = IndexDirectFile(10, index_file, main_file, overflow_file, 0.6)
        self.index_direct_file.upload_data()

    def test_negative(self):
        print("Remove tests")
        result = self.index_direct_file.add(1, 'gsg')
        self.assertEqual(result, None)

    def test_positive(self):
        self.index_direct_file.add(11, 'gsg')
        self.assertEqual(self.index_direct_file.main_lines[10], 'gsg')
        self.assertEqual(self.index_direct_file.lines[10], ['0000000011', '0000000011'])

    def test_edge_values(self):
        self.index_direct_file.lines[9] = ["000000None", "000000None"]
        self.index_direct_file.lines[8] = ["000000None", "000000None"]
        self.index_direct_file.add(9, 'gsg')
        self.assertEqual(self.index_direct_file.main_lines[10], 'gsg')
        self.assertEqual(self.index_direct_file.lines[8], ["0000000009", "0000000011"])


if __name__ == '__main__':
    unittest.main()
