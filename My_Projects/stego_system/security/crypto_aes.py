from Crypto.Cipher import AES
import base64

class CryptoAES:
    def __init__(self, key):
        self.key = key

    def pad(self, data):
        pad_len = 16 - len(data) % 16
        return data + chr(pad_len) * pad_len

    def unpad(self, data):
        return data[:-ord(data[-1])]

    def encrypt(self, text: str) -> str:
        cipher = AES.new(self.key, AES.MODE_ECB)
        encrypted = cipher.encrypt(self.pad(text).encode())
        return base64.b64encode(encrypted).decode()

    def decrypt(self, encrypted_text: str) -> str:
        cipher = AES.new(self.key, AES.MODE_ECB)
        decoded = base64.b64decode(encrypted_text)
        decrypted = cipher.decrypt(decoded).decode()
        return self.unpad(decrypted)