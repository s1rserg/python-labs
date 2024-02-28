def clear_files(files):
    for file in files:
        try:
            with open(file, 'w'):
                pass
        except FileNotFoundError:
            print(f"The file '{file}' does not exist.")
        except Exception as e:
            print(f"An error occurred while clearing '{file}': {str(e)}")


def validate_positive_integer(n):
    try:
        value = int(n)
        if value > 0:
            return True
        else:
            return False
    except ValueError:
        return False
