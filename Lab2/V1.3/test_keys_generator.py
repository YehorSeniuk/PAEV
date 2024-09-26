import unittest
from kesy_generator import KeysGenerator, PublicKey, PrivateKey


class TestKeysGenerator(unittest.TestCase):

    def test_generate_rsa_keys_returns_public_key_instance(self):
        public_key, _ = KeysGenerator.generate_rsa_keys()
        self.assertIsInstance(public_key, PublicKey)

    def test_generate_rsa_keys_returns_private_key_instance(self):
        _, private_key = KeysGenerator.generate_rsa_keys()
        self.assertIsInstance(private_key, PrivateKey)

    def test_public_and_private_key_have_same_n(self):
        public_key, private_key = KeysGenerator.generate_rsa_keys()
        self.assertEqual(public_key.n, private_key.n)


    def test_public_key_has_e_property(self):
        public_key, _ = KeysGenerator.generate_rsa_keys()
        self.assertTrue(hasattr(public_key, 'e'))

    def test_public_key_has_n_property(self):
        public_key, _ = KeysGenerator.generate_rsa_keys()
        self.assertTrue(hasattr(public_key, 'n'))

    def test_public_key_e_is_integer(self):
        public_key, _ = KeysGenerator.generate_rsa_keys()
        self.assertIsInstance(public_key.e, int)

    def test_public_key_n_is_integer(self):
        public_key, _ = KeysGenerator.generate_rsa_keys()
        self.assertIsInstance(public_key.n, int)

    def test_private_key_has_d_property(self):
        _, private_key = KeysGenerator.generate_rsa_keys()
        self.assertTrue(hasattr(private_key, 'd'))

    def test_private_key_has_n_property(self):
        _, private_key = KeysGenerator.generate_rsa_keys()
        self.assertTrue(hasattr(private_key, 'n'))

    def test_private_key_d_is_integer(self):
        _, private_key = KeysGenerator.generate_rsa_keys()
        self.assertIsInstance(int(private_key.d), int)

    def test_private_key_n_is_integer(self):
        _, private_key = KeysGenerator.generate_rsa_keys()
        self.assertIsInstance(private_key.n, int)

    def test_public_key_str_method(self):
        public_key, _ = KeysGenerator.generate_rsa_keys()
        self.assertTrue(str(public_key).startswith('PublicKey('))

    def test_private_key_str_method(self):
        _, private_key = KeysGenerator.generate_rsa_keys()
        self.assertTrue(str(private_key).startswith('PrivateKey('))


if __name__ == '__main__':
    unittest.main()
