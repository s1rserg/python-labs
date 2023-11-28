import matplotlib.pyplot as plt


def read_and_parse_file(file_path):
    try:
        with open(file_path, 'r') as file:
            data = []
            for line_number, line in enumerate(file, start=1):
                values = [value.strip() for value in line.split(',')]

                if len(values) != 2:
                    raise ValueError(
                        f"Error in line {line_number}: Each line should contain exactly two values separated by a comma and space.")

                try:
                    values = [int(value) for value in values]
                except ValueError:
                    raise ValueError(f"Error in line {line_number}: Values must be valid integers.")

                data.append(values)

            if len(data) % 4 != 0:
                raise ValueError("Error: The number of lines in the file must be a multiple of 4.")
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")
    except Exception as e:
        raise e


def graph(x_values, y_values):
    plt.plot(x_values, y_values, label='Графік залежності якості розв`язку від числа ітерацій')
    plt.xlabel('Число ітерацій')
    plt.ylabel('Якість розв`язку')
    plt.xticks(x_values[::2])
    plt.yticks(list(set(y_values)))
    plt.show()
