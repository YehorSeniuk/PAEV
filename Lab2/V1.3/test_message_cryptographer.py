import random
import unittest
from kesy_generator import KeysGenerator
from message_cryptographer import MessageCryptographer

class TestMessageCryptographer(unittest.TestCase):

    def setUp(self):
        self.public_key, self.private_key = KeysGenerator.generate_rsa_keys()

    def test_encode_message_returns_encrypted_message(self):
        m = 123
        encrypted_message = MessageCryptographer.encode_message(m, self.public_key)
        self.assertTrue(0 <= encrypted_message < self.public_key.n)

    def test_decode_message_returns_original_message(self):
        m = 123
        encrypted_message = MessageCryptographer.encode_message(m, self.public_key)
        decrypted_message = MessageCryptographer.decode_message(encrypted_message, self.private_key)
        self.assertEqual(m, decrypted_message)

    def test_encryption_decryption_with_random_message(self):
        m = random.randint(1, self.public_key.n - 1)
        encrypted_message = MessageCryptographer.encode_message(m, self.public_key)
        decrypted_message = MessageCryptographer.decode_message(encrypted_message, self.private_key)
        self.assertEqual(m, decrypted_message)

    def test_encryption_of_large_message(self):
        m = self.public_key.n - 1
        encrypted_message = MessageCryptographer.encode_message(m, self.public_key)
        decrypted_message = MessageCryptographer.decode_message(encrypted_message, self.private_key)
        self.assertEqual(m, decrypted_message)

    def test_encryption_of_small_message(self):
        m = 1
        encrypted_message = MessageCryptographer.encode_message(m, self.public_key)
        decrypted_message = MessageCryptographer.decode_message(encrypted_message, self.private_key)
        self.assertEqual(m, decrypted_message)

if __name__ == '__main__':
    unittest.main()
