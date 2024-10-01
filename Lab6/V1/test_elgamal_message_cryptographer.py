import unittest
from unittest.mock import patch
from elgamal_message_cryptographer import ElGamalMessageCryptographer, ElGamalPublicKey, ElGamalPrivateKey, CipherPairs
from copy import deepcopy
from sympy import isprime


class TestElGamalMessageCryptographer(unittest.TestCase):

    def setUp(self):
        self.public_key, self.private_key = ElGamalMessageCryptographer.generate_keys()
        self.message = "Hello"

    @patch('random.randrange')
    def test_generate_keys(self, mock_randrange):
        mock_randrange.side_effect = [137, 123]  # mocking random prime and private key
        public_key, private_key = ElGamalMessageCryptographer.generate_keys()
        self.assertIsInstance(public_key, ElGamalPublicKey)
        self.assertIsInstance(private_key, ElGamalPrivateKey)
        self.assertTrue(public_key.p > 0)
        self.assertTrue(public_key.g > 0)
        self.assertTrue(public_key.y > 0)
        self.assertTrue(private_key.x > 0)

    def test_generate_prime(self):
        prime = ElGamalMessageCryptographer.generate_prime(200)
        self.assertTrue(prime < 200)
        self.assertTrue(prime > 137)
        self.assertTrue(isprime(prime))

    def test_encrypt(self):
        encrypted = ElGamalMessageCryptographer.encrypt(self.message, self.public_key)
        self.assertIsInstance(encrypted, CipherPairs)
        self.assertEqual(len(encrypted.cipher_pairs), len(self.message))
        for a, b in encrypted:
            self.assertIsInstance(a, int)
            self.assertIsInstance(b, int)

    def test_decrypt(self):
        encrypted = ElGamalMessageCryptographer.encrypt(self.message, self.public_key)
        decrypted_message = ElGamalMessageCryptographer.decrypt(encrypted, self.public_key.p, self.private_key.x)
        self.assertEqual(self.message, decrypted_message)

    def test_large_message_encryption_decryption(self):
        large_message = "This is a large test message for ElGamal encryption"
        encrypted = ElGamalMessageCryptographer.encrypt(large_message, self.public_key)
        decrypted = ElGamalMessageCryptographer.decrypt(encrypted, self.public_key.p, self.private_key.x)
        self.assertEqual(large_message, decrypted)

    def test_encrypt_empty_message(self):
        empty_message = ""
        encrypted = ElGamalMessageCryptographer.encrypt(empty_message, self.public_key)
        self.assertEqual(len(encrypted.cipher_pairs), 0)
        decrypted = ElGamalMessageCryptographer.decrypt(encrypted, self.public_key.p, self.private_key.x)
        self.assertEqual(empty_message, decrypted)

    def test_negative_prime_generation_limit(self):
        with self.assertRaises(ValueError):
            ElGamalMessageCryptographer.generate_prime(-1000)

    @patch('random.randrange')
    def test_encryption_with_mocked_k(self, mock_randrange):
        mock_randrange.return_value = 42  # Mock the random k value
        encrypted = ElGamalMessageCryptographer.encrypt(self.message, self.public_key)
        self.assertEqual(len(encrypted.cipher_pairs), len(self.message))
        decrypted = ElGamalMessageCryptographer.decrypt(encrypted, self.public_key.p, self.private_key.x)
        self.assertEqual(self.message, decrypted)

    def test_cipherpairs_structure(self):
        encrypted = ElGamalMessageCryptographer.encrypt(self.message, self.public_key)
        cipher_pairs = encrypted.cipher_pairs
        self.assertEqual(len(cipher_pairs), len(self.message))
        for a, b in cipher_pairs:
            self.assertIsInstance(a, int)
            self.assertIsInstance(b, int)

    def test_public_key_representation(self):
        expected_repr = f'ElGamalPublicKey({self.public_key.p}, {self.public_key.g}, {self.public_key.y})'
        self.assertEqual(repr(self.public_key), expected_repr)

    def test_private_key_operations(self):
        other = 5
        self.assertEqual(self.private_key + other, self.private_key.x + other)
        self.assertEqual(self.private_key - other, self.private_key.x - other)
        self.assertEqual(self.private_key * other, self.private_key.x * other)
        self.assertEqual(self.private_key % other, self.private_key.x % other)
        self.assertEqual(pow(self.private_key, other, self.public_key.p), pow(self.private_key.x, other, self.public_key.p))

    def test_deepcopy_cipherpairs(self):
        encrypted = ElGamalMessageCryptographer.encrypt(self.message, self.public_key)
        copied_cipherpairs = deepcopy(encrypted.cipher_pairs)
        self.assertEqual(copied_cipherpairs, encrypted.cipher_pairs)

    def test_iter_cipherpairs(self):
        encrypted = ElGamalMessageCryptographer.encrypt(self.message, self.public_key)
        for a, b in encrypted:
            self.assertIsInstance(a, int)
            self.assertIsInstance(b, int)

    def test_cipherpairs_repr(self):
        encrypted = ElGamalMessageCryptographer.encrypt(self.message, self.public_key)
        expected_repr = f'{[block for block in encrypted]}'
        self.assertEqual(repr(encrypted), expected_repr)


if __name__ == '__main__':
    unittest.main()
