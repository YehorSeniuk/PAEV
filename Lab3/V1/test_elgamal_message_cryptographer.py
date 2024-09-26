import unittest
from elgamal_message_cryptographer import ElGamalMessageCryptographer, ElGamalPublicKey, ElGamalPrivateKey, CipherPairs
from sympy import isprime

class TestElGamalMessageCryptographer(unittest.TestCase):

    def setUp(self):
        self.public_key, self.private_key = ElGamalMessageCryptographer.generate_keys()

    def test_key_generation_instance(self):
        self.assertIsInstance(self.public_key, ElGamalPublicKey)
        self.assertIsInstance(self.private_key, ElGamalPrivateKey)

    def test_key_generation_prime(self):
        self.assertTrue(isprime(self.public_key.p))

    def test_key_generation_generator(self):
        self.assertGreater(self.public_key.g, 1)
        self.assertLess(self.public_key.g, self.public_key.p)

    def test_key_generation_y(self):
        self.assertGreater(self.public_key.y, 1)
        self.assertLess(self.public_key.y, self.public_key.p)

    def test_encrypt_message(self):
        message = "Hello, ElGamal!"
        cipher_pairs = ElGamalMessageCryptographer.encrypt(message, self.public_key)
        self.assertIsInstance(cipher_pairs, CipherPairs)

    def test_decrypt_message(self):
        message = "Hello, ElGamal!"
        cipher_pairs = ElGamalMessageCryptographer.encrypt(message, self.public_key)
        decrypted_message = ElGamalMessageCryptographer.decrypt(cipher_pairs.cipher_pairs, self.public_key.p, self.private_key.x)
        self.assertEqual(decrypted_message, message)

    def test_encryption_is_not_same_as_original(self):
        message = "Hello, ElGamal!"
        cipher_pairs = ElGamalMessageCryptographer.encrypt(message, self.public_key)
        encrypted_message = ''.join(f'{a},{b} ' for a, b in cipher_pairs.cipher_pairs)
        self.assertNotEqual(encrypted_message.strip(), message)

    def test_decrypt_invalid_cipher(self):
        invalid_cipher_pairs = [(0, 0), (self.public_key.p, self.public_key.p)]
        decrypted_message = ElGamalMessageCryptographer.decrypt(invalid_cipher_pairs, self.public_key.p, self.private_key.x)
        self.assertNotEqual(decrypted_message, "Hello, ElGamal!")

if __name__ == '__main__':
    unittest.main()
