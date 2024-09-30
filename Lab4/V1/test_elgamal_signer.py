import unittest
from elgamal_signer import ElGamalSigner, ElGamalPublicKey, ElGamalPrivateKey


class TestElGamalSigner(unittest.TestCase):

    def setUp(self):
        self.public_key, self.private_key = ElGamalSigner.generate_keys()
        self.message = "Test message"

    def test_generate_keys(self):
        public_key, private_key = ElGamalSigner.generate_keys()

        self.assertIsInstance(public_key, ElGamalPublicKey)
        self.assertIsInstance(private_key, ElGamalPrivateKey)

        self.assertTrue(1 < public_key.g < public_key.p)

        self.assertEqual(pow(public_key.g, private_key.x, public_key.p), public_key.y)

    def test_sign_message(self):
        r, s = ElGamalSigner.sign_message(self.private_key, self.public_key, self.message)

        self.assertTrue(0 < r < self.public_key.p)
        self.assertTrue(0 < s < self.public_key.p - 1)


    def test_verify_signature(self):
        self.public_key, self.private_key = ElGamalSigner.generate_keys()
        signature= ElGamalSigner.sign_message(self.private_key, self.public_key, self.message)
        is_valid = ElGamalSigner.verify_signature(self.public_key, self.message, signature)
        self.assertTrue(is_valid)


    def test_invalid_signature(self):
        fake_signature = (1, 1)
        is_valid = ElGamalSigner.verify_signature(self.public_key, self.message, fake_signature)

        self.assertFalse(is_valid)

    def test_signature_with_modified_message(self):
        signature = ElGamalSigner.sign_message(self.private_key, self.public_key, self.message)
        is_valid = ElGamalSigner.verify_signature(self.public_key, "Modified message", signature)

        self.assertFalse(is_valid)


if __name__ == '__main__':
    unittest.main()
