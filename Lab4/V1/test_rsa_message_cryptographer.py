import unittest
from sympy import gcd
from rsa_message_cryptographer import RSAMessageCryptographer, RSAPublicKey, RSAPrivateKey


class TestRSAMessageCryptographer(unittest.TestCase):

    def setUp(self):
        self.public_key, self.private_key = RSAMessageCryptographer.generate_keys()
        self.message = 123

    def test_generate_keys(self):
        public_key, private_key = RSAMessageCryptographer.generate_keys()

        self.assertIsInstance(public_key, RSAPublicKey)
        self.assertIsInstance(private_key, RSAPrivateKey)

        self.assertEqual(public_key.n, private_key.n)

        p = 881
        q = 947
        phi_n = (p - 1) * (q - 1)
        self.assertEqual((public_key.e * private_key.d) % phi_n, 1)

    def test_encode_decode_message(self):
        encoded_message = RSAMessageCryptographer.encode_message(self.message, self.public_key)
        decoded_message = RSAMessageCryptographer.decode_message(encoded_message, self.private_key)

        self.assertEqual(decoded_message, self.message)

    def test_large_message(self):
        large_message = self.public_key.n - 1
        encoded_message = RSAMessageCryptographer.encode_message(large_message, self.public_key)
        decoded_message = RSAMessageCryptographer.decode_message(encoded_message, self.private_key)

        self.assertEqual(decoded_message, large_message)

    def test_invalid_public_key(self):
        invalid_public_key = RSAPublicKey(e=123456, n=self.public_key.n)
        encoded_message = RSAMessageCryptographer.encode_message(self.message, invalid_public_key)
        decoded_message = RSAMessageCryptographer.decode_message(encoded_message, self.private_key)

        self.assertNotEqual(decoded_message, self.message)

    def test_edge_case_message_zero(self):
        encoded_message = RSAMessageCryptographer.encode_message(0, self.public_key)
        decoded_message = RSAMessageCryptographer.decode_message(encoded_message, self.private_key)

        self.assertEqual(decoded_message, 0)

    def test_phi_n_coprime(self):
        p = 881
        q = 947
        phi_n = (p - 1) * (q - 1)
        e = self.public_key.e

        self.assertEqual(gcd(e, phi_n), 1)

    def test_decryption_with_wrong_private_key(self):
        encoded_message = RSAMessageCryptographer.encode_message(self.message, self.public_key)
        wrong_private_key = RSAPrivateKey(d=self.private_key.d + 1, n=self.private_key.n)
        decoded_message = RSAMessageCryptographer.decode_message(encoded_message, wrong_private_key)

        self.assertNotEqual(decoded_message, self.message)

    def test_public_key_iteration(self):
        e, n = tuple(self.public_key)
        self.assertEqual(e, self.public_key.e)
        self.assertEqual(n, self.public_key.n)

    def test_private_key_iteration(self):
        d, n = tuple(self.private_key)
        self.assertEqual(d, self.private_key.d)
        self.assertEqual(n, self.private_key.n)

if __name__ == '__main__':
    unittest.main()
