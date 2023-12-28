class Base62EncodeDecode:
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

    @staticmethod
    def convert_to_base62(number: int) -> str:
        base62 = ""
        while number > 0:
            remainder = number % 62
            base62 = str(Base62EncodeDecode.ALPHABET[remainder]) + base62
            number = number // 62
        return base62

    @staticmethod
    def base62_to_decimal(base62: str) -> str:
        decimal_value = 0
        for i, char in enumerate(base62):
            position_value = Base62EncodeDecode.ALPHABET.index(char)
            power_of_62 = len(base62) - i - 1
            decimal_value += position_value * (62**power_of_62)
        return decimal_value

class Base62CounterUtils:
    def __init__(self):
        self.ltos = {}
        self.stol = {}
        self.COUNTER = 100000000000
        self.ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def generate_random_short_url(self, url):
        short_url = self._base10_to_base62(self.COUNTER)
        self.ltos[url] = self.COUNTER
        self.stol[self.COUNTER] = url
        self.COUNTER += 1
        return "http://tiny.url/" + short_url

    def search_long_url(self, url):
        url = url[len("http://tiny.url/"):]
        n = self._base62_to_base10(url)
        return self.stol.get(n)

    def _base62_to_base10(self, s):
        n = 0
        for i in range(len(s)):
            n = n * 62 + self._convert(s[i])
        return n

    def _convert(self, c):
        if '0' <= c <= '9':
            return ord(c) - ord('0')
        if 'a' <= c <= 'z':
            return ord(c) - ord('a') + 10
        if 'A' <= c <= 'Z':
            return ord(c) - ord('A') + 36
        return -1

    def _base10_to_base62(self, n):
        result = []
        while n != 0:
            result.insert(0, self.ALPHABET[n % 62])
            n //= 62
        while len(result) != 7:
            result.insert(0, '0')
        return ''.join(result)