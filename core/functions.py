import random
import string

promocode_chars = list(string.ascii_uppercase + string.digits)


def get_random_id() -> int:
    return str(random.randrange(100000000000, 999999999999))


def get_random_promocode() -> str:
    promocode = ""
    for _ in range(5):
        promocode += random.choice(promocode_chars)
    return promocode
