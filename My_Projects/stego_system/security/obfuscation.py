import random
import string

class Obfuscation:

    def noise(self, text: str) -> str:
        junk = ''.join(random.choices(string.ascii_letters, k=5))
        return text + junk

    def de_noise(self, text: str) -> str:
        return text[:-5]