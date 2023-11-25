def validate_positive_integer(n, max_len):
    if len(n) > max_len or len(n) == 0:
        return False, "Length of a key should be between 1 and 10 symbols"
    try:
        value = int(n)
        if value > 0:
            return True, "Success"
        else:
            return False, "Key cannot be less than 1"
    except ValueError:
        return False, "Inappropriate symbols in key"