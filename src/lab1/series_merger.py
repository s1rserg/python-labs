import os


class SeriesMerger:
    def __init__(self, input_files, output_files, size):
        self.input_files = input_files
        self.output_files = output_files
        self.size = size

    def merge_series(self):
        inputs = [open(input_file, 'r') for input_file in self.input_files]
        outputs = [open(output_file, 'w') for output_file in self.output_files]

        num_of_files = len(inputs)
        values = [None] * num_of_files  # зчитані значення
        last_values = [None] * num_of_files  # попередні зчитані значення
        series_ends = [False] * num_of_files  # чи закінчилась n-та серія у файлі
        buffer = [None] * num_of_files  # буфер зчитаних значень (якщо серія скінчилась, то значення потрапляє сюди)
        while True:
            if num_of_files == 0:
                break
            for i in range(num_of_files):
                if not values[i] and not series_ends[i]:
                    if buffer[i]:  # якщо у буфері щось є, то воно має бути зчитане першим
                        line = str(buffer[i])
                        buffer[i] = None
                    else:
                        line = inputs[i].readline()
                    if not line.strip():  # якщо зчитано пустий рядок, значить файл закінчився
                        num_of_files -= 1
                        inputs[i].close()
                        del inputs[i]
                        del values[i]
                        del last_values[i]
                        del series_ends[i]
                        break
                    else:
                        try:
                            values[i] = int(line)
                        except ValueError:
                            for file in inputs + outputs:
                                file.close()
                            raise ValueError(f"Invalid value in file {self.input_files[i]}: {line}")
                        if last_values[i] and values[i] < last_values[i]:  # перевірка на кінець серії
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
            if any(element for element in values):  # запис у файл
                min_value = min(v for v in values if v)
                outputs[0].write(str(min_value) + '\n')
                values[values.index(min_value)] = None

        for file in inputs + outputs:
            file.close()

        if any(os.stat(file).st_size != 0 for file in self.output_files[1:]):
            # якщо b2-bn або c2-cn не пусті, то зливаємо знову
            self.input_files, self.output_files = self.output_files, self.input_files
            self.merge_series()
