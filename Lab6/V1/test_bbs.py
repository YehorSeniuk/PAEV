import unittest
from unittest.mock import patch
import sympy
from bbs import BBSMessageCryptographer, BBSPublicKey, BBSPrivateKey, BBSBits, BBSConverter


class TestBBSMessageCryptographer(unittest.TestCase):

    def setUp(self):
        self.public_key, self.private_key = BBSMessageCryptographer.generate_keys()
        self.message = 12345

    def test_generate_primes(self):
        p, q = BBSMessageCryptographer.generate_primes()
        self.assertTrue(sympy.isprime(p))
        self.assertTrue(sympy.isprime(q))

    def test_generate_keys(self):
        public_key, private_key = BBSMessageCryptographer.generate_keys()
        self.assertIsInstance(public_key, BBSPublicKey)
        self.assertIsInstance(private_key, BBSPrivateKey)

    @patch('random.randint')
    def test_generate_x(self, mock_randint):
        mock_randint.return_value = 123
        x = BBSMessageCryptographer.generate_x(499 * 547)
        self.assertEqual(x, 123)

    def test_bbs_generate_bits(self):
        num_bits = 8
        bits = BBSMessageCryptographer.bbs_generate_bits(self.public_key, num_bits)
        self.assertEqual(len(bits), num_bits)
        self.assertTrue(all(bit == 0 or bit == 1 for bit in bits))

    def test_encrypt_integer(self):
        encrypted_message = BBSMessageCryptographer.encrypt_integer(self.message, self.public_key)
        self.assertIsInstance(encrypted_message, BBSBits)
        self.assertNotEqual(self.message, int(encrypted_message))

    def test_decrypt_integer(self):
        encrypted_message = BBSMessageCryptographer.encrypt_integer(self.message, self.public_key)
        decrypted_message = BBSMessageCryptographer.decrypt_integer(encrypted_message, self.public_key)
        self.assertEqual(self.message, decrypted_message)

    def test_bbs_bits_conversion(self):
        bits = BBSConverter.int_to_bits(self.message)
        self.assertIsInstance(bits, list)
        self.assertEqual(self.message, BBSConverter.bits_to_int(bits))

    def test_bbsbits_initialization(self):
        bbs_bits = BBSBits(_int=self.message)
        self.assertEqual(int(bbs_bits), self.message)
        self.assertEqual(len(bbs_bits), len(bin(self.message)) - 2)  # bin() -> '0b' prefix

    def test_bbsbits_encryption_xor(self):
        message_bits = BBSBits(_int=self.message)
        bits = [1 for _ in range(len(message_bits))]
        encrypted_bits = [(m ^ b) for m, b in zip(message_bits, bits)]
        self.assertNotEqual(int(message_bits), BBSConverter.bits_to_int(encrypted_bits))

    def test_large_number_encryption_decryption(self):
        large_message = 9876543210
        encrypted_message = BBSMessageCryptographer.encrypt_integer(large_message, self.public_key)
        decrypted_message = BBSMessageCryptographer.decrypt_integer(encrypted_message, self.public_key)
        self.assertEqual(large_message, decrypted_message)

    def test_zero_encryption_decryption(self):
        encrypted_message = BBSMessageCryptographer.encrypt_integer(0, self.public_key)
        decrypted_message = BBSMessageCryptographer.decrypt_integer(encrypted_message, self.public_key)
        self.assertEqual(0, decrypted_message)

    def test_negative_number_encryption(self):
        with self.assertRaises(ValueError):
            BBSMessageCryptographer.encrypt_integer(-123, self.public_key)


if __name__ == '__main__':
    unittest.main()
