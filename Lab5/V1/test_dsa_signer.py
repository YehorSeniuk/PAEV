import unittest
from dsa_signer import DSASigner, DSASignature, DSAParams, DSAPublicKey, DSAPrivateKey

class TestDSASigner(unittest.TestCase):

    def setUp(self):
        self.params, self.public_key, self.private_key = DSASigner.generate_params_and_keys()
        self.message = str.encode("Pes Patron", "ascii")

    def test_sign_returns_signature(self):
        signature = DSASigner.sign(self.message, self.params, self.private_key)
        self.assertIsInstance(signature, DSASignature)

    def test_verify_signature_returns_true(self):
        signature = DSASigner.sign(self.message, self.params, self.private_key)
        is_valid = DSASigner.verify(self.message, signature, self.params, self.public_key.y)
        self.assertTrue(is_valid)

    def test_verify_signature_returns_false_for_invalid_signature(self):
        signature = DSASigner.sign(self.message, self.params, self.private_key)
        invalid_signature = DSASignature(signature.r + 1, signature.s)
        is_valid = DSASigner.verify(self.message, invalid_signature, self.params, self.public_key.y)
        self.assertFalse(is_valid)

    def test_validate_params_returns_true_for_valid_params(self):
        valid = DSASigner.validate_params(self.params)
        self.assertTrue(valid)

    def test_validate_params_returns_false_for_invalid_params(self):
        invalid_params = DSAParams(1, 1, 1)
        valid = DSASigner.validate_params(invalid_params)
        self.assertFalse(valid)

    def test_generate_params_and_keys(self):
        params, public_key, private_key = DSASigner.generate_params_and_keys()
        self.assertIsInstance(params, DSAParams)
        self.assertIsInstance(private_key, DSAPrivateKey)
        self.assertIsInstance(public_key, DSAPublicKey)

    def test_generate_p_q(self):
        L, N = 1024, 160
        p, q = DSASigner.generate_p_q(L, N)
        self.assertGreater(p, 2 ** (L - 1))
        self.assertGreater(q, 2 ** (N - 1))

    def test_generate_g(self):
        g = DSASigner.generate_g(self.params.p, self.params.q)
        self.assertGreater(g, 1)
        self.assertLess(g, self.params.p)

if __name__ == '__main__':
    unittest.main()