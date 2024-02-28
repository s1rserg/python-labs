class SeriesSplitter:
    def __init__(self, input_file, output_files):
        self.input_file = input_file
        self.output_files = output_files

    def split_series(self):
        current_series = 0
        last_num = None
        outputs = [open(output_file, 'w') for output_file in self.output_files]

        with open(self.input_file, 'r') as f:
            for line in f:
                try:
                    num = int(line.strip())
                except ValueError:
                    for file in outputs:
                        file.close()
                    raise ValueError(f"Invalid value in input file: {line}")
                if last_num is not None and num < last_num:  # якщо попереднє число більше наступного, серія закінчилась
                    current_series = (current_series + 1) % len(outputs)
                outputs[current_series].write(f"{num}\n")
                last_num = num

        for file in outputs:
            file.close()
