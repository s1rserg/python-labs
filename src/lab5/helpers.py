def validate_positive_integer(n):
    try:
        value = int(n)
        if value > 0:
            return True
        else:
            return False
    except ValueError:
        return False

