from re import findall


def comma_separator(list_: list) -> str:
    """Separates commas using simple ``.join()`` function and analysis based on length of the list taken as argument.

    Args:
        list_: Takes a list of elements as an argument.

    Returns:
        str:
        Comma separated list of elements.
    """
    return ', and '.join([', '.join(list_[:-1]), list_[-1]] if len(list_) > 2 else list_)


def extract_nos(input_: str) -> float:
    """Extracts number part from a string.

    Args:
        input_: Takes string as an argument.

    Returns:
        float:
        Float values.
    """
    return float('.'.join(findall(r"\d+", input_)))


def format_nos(input_: float) -> int:
    """Removes ``.0`` float values.

    Args:
        input_: Int if found, else returns the received float value.

    Returns:
        int:
        Formatted integer.
    """
    return int(input_) if isinstance(input_, float) and input_.is_integer() else input_


def extract_str(input_: str) -> str:
    """Extracts strings from the received input.

    Args:
        input_: Takes a string as argument.

    Returns:
        str:
        A string after removing special characters.
    """
    return ''.join([i for i in input_ if not i.isdigit() and i not in [',', '.', '?', '-', ';', '!', ':']]).strip()
