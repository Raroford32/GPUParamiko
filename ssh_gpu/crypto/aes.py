from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

class AES:
    def __init__(self, key):
        if len(key) not in (16, 24, 32):
            raise ValueError("Invalid key size. Key must be 16, 24, or 32 bytes long.")
        self.key = key
        self.backend = default_backend()

    def encrypt(self, plaintext):
        iv = os.urandom(16)  # Generate a 16-byte IV
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        return iv + ciphertext  # Prepend IV to ciphertext

    def decrypt(self, data):
        iv = data[:16]  # Extract the 16-byte IV
        ciphertext = data[16:]  # Get the actual ciphertext
        cipher = Cipher(algorithms.AES(self.key), modes.CFB(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()
