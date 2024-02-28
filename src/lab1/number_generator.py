import random


class NumberGenerator:
    def __init__(self, filename, size):
        self.filename = filename
        self.size = size

    def generate(self):
        numbers_per_chunk = self.size // (10 ** 6)
        chunk = ''
        with open(self.filename, 'w') as f:
            while f.tell() < self.size:
                chunk += '\n'.join(str(random.randint(1, 1000)) for _ in range(numbers_per_chunk)) + '\n'
                f.write(chunk)
                chunk = ''
        print("Random numbers generated!")
