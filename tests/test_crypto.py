import unittest
from ssh_gpu.crypto import RSA, AES

class TestRSA(unittest.TestCase):
    def setUp(self):
        self.rsa = RSA()
        self.rsa.generate_keys()

    def test_encrypt_decrypt(self):
        message = "Hello, World!"
        encrypted = self.rsa.encrypt(message)
        decrypted = self.rsa.decrypt(encrypted)
        self.assertEqual(message, decrypted)

class TestAES(unittest.TestCase):
    def setUp(self):
        self.key = b'0123456789abcdef'
        self.aes = AES(self.key)

    def test_encrypt_decrypt(self):
        message = b"Hello, World!"
        encrypted = self.aes.encrypt(message)
        decrypted = self.aes.decrypt(encrypted)
        self.assertEqual(message, decrypted)

if __name__ == '__main__':
    unittest.main()
