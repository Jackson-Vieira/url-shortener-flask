import random

"""
--- Base62 Conversion ---
Blog: https://dev.to/joshduffney/what-is-base62-conversion-13o0
"""


class RandomUtils:
    NUM_CHARS_SHORT_LINK = 7
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

    @staticmethod
    def generate_random_short_url():
        """
        Short url from random numbers
        """

        result = ""
        for _ in range(RandomUtils.NUM_CHARS_SHORT_LINK):
            random_index = random.randint(a=0, b=len(RandomUtils.ALPHABET) - 1)
            result += str(RandomUtils.ALPHABET[random_index])
        return result
    
class Base62Utils:
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

    @staticmethod
    def convert_to_base62(number: int) -> str:
        base62 = ""
        while number > 0:
            remainder = number % 62
            base62 = str(Base62Utils.ALPHABET[remainder]) + base62
            number = number // 62
        return base62

    @staticmethod
    def base62_to_decimal(base62: str) -> str:
        decimal_value = 0
        for i, char in enumerate(base62):
            position_value = Base62Utils.ALPHABET.index(char)
            power_of_62 = len(base62) - i - 1
            decimal_value += position_value * (62**power_of_62)
        return decimal_value