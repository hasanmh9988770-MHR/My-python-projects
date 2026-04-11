import os
import hashlib

class KeyManager:
    def __init__(self):
        pass

    def derive_key(self, password: str) -> bytes:
        """Convert password → 32 byte AES key"""
        return hashlib.sha256(password.encode()).digest()

    def generate_salt(self):
        return os.urandom(16)