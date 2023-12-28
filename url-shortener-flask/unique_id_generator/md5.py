import hashlib
import secrets

class MD5Utils:
    SHORT_URL_CHAR_SIZE = 7

    @staticmethod
    def convert(long_url):
        try:
            digest = hashlib.md5(long_url.encode())
            hex_string = digest.hexdigest()
            return hex_string
        except Exception as e:
            raise RuntimeError(e)

    @staticmethod
    def generate_random_short_url(long_url):
        hash_value = MD5Utils.convert(long_url)
        number_of_chars_in_hash = len(hash_value)

        for counter in range(number_of_chars_in_hash - MD5Utils.SHORT_URL_CHAR_SIZE + 1):
            substring = hash_value[counter : counter + MD5Utils.SHORT_URL_CHAR_SIZE]

            # check if substring exists in the database
            if not DB.exists(substring):
                return substring

        # If no unique substring is found, generate a random one
        return MD5Utils.generate_random_short_url(long_url + secrets.token_hex(MD5Utils.SHORT_URL_CHAR_SIZE // 2))

# Dummy DB class for illustration purposes
class DB:
    @staticmethod
    def exists(substring):
        # Placeholder function, replace with actual logic to check if substring exists in the database
        return False