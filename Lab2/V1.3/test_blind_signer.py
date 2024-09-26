import unittest
from blind_signer import BlindSigner, MaskedMessage
from kesy_generator import PublicKey, PrivateKey

class TestBlindSigner(unittest.TestCase):

    def setUp(self):
        self.m = 123
        self.public_key = PublicKey(65537, 3233)
        self.private_key = PrivateKey(2753, 3233)

    def test_mask_message_returns_masked_message_instance(self):
        masked_message = BlindSigner.mask_message(self.m, self.public_key)
        self.assertIsInstance(masked_message, MaskedMessage)

    def test_mask_message_computes_correctly(self):
        masked_message = BlindSigner.mask_message(self.m, self.public_key)
        self.assertTrue(0 <= masked_message.masked_m < self.public_key.n)

    def test_unmask_message_computes_correctly(self):
        masked_message = BlindSigner.mask_message(self.m, self.public_key)
        unmasked_message = BlindSigner.unmask_message(masked_message, self.public_key)
        self.assertEqual(self.m, unmasked_message)

    def test_mask_sign_computes_correctly(self):
        masked_message = BlindSigner.mask_message(self.m, self.public_key)
        masked_signature = BlindSigner.mask_sign(masked_message, self.private_key)
        self.assertTrue(0 <= masked_signature < self.public_key.n)

    def test_verify_sign_returns_true_for_valid_signature(self):
        masked_message = BlindSigner.mask_message(self.m, self.public_key)
        masked_signature = BlindSigner.mask_sign(masked_message, self.private_key)
        unmasked_signature = BlindSigner.unmask_sign(masked_signature, masked_message, self.private_key)
        self.assertTrue(BlindSigner.verify_sign(unmasked_signature, self.m, self.public_key))

    def test_verify_sign_returns_false_for_invalid_signature(self):
        invalid_signature = 456
        self.assertFalse(BlindSigner.verify_sign(invalid_signature, self.m, self.public_key))

if __name__ == '__main__':
    unittest.main()
