from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os

class AES:
    def __init__(self, key):
        if len(key) not in (16, 24, 32):
            raise ValueError("Invalid key size. Key must be 16, 24, or 32 bytes long.")
        self.key = key
        self.backend = default_backend()

    def encrypt(self, plaintext, use_gpu=False):
        iv = os.urandom(16)  # Generate a 16-byte IV
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext) + padder.finalize()
        
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        return iv + ciphertext  # Prepend IV to ciphertext

    def decrypt(self, data):
        if len(data) < 16:
            raise ValueError("Input data must be at least 16 bytes long (IV)")
        iv = data[:16]  # Extract the 16-byte IV
        ciphertext = data[16:]  # Get the actual ciphertext
        
        if len(ciphertext) == 0:
            return b""  # Return empty bytes for empty ciphertext
        
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        unpadder = padding.PKCS7(128).unpadder()
        try:
            plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
        except ValueError:
            # If unpadding fails, return the padded plaintext
            plaintext = padded_plaintext
        return plaintext
