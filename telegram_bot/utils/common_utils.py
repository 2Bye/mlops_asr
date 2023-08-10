import random
import string


def get_random_string(length: int) -> str:
    """Generate random string

    Args:
        length (int): the length of your random string

    Returns:
        result_str (str): random string
    """
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str
