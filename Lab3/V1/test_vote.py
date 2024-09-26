import unittest
from unittest.mock import patch
from vote import Vote


class TestVote(unittest.TestCase):

    def setUp(self):
        self.private_id = 'private_id'
        self.registration_id = 'registration_id'
        self.candidate_id = 'candidate_id'
        self.elgamal_public_key = 'elgamal_public_key'
        self.params = 'params'
        self.dsa_public_key = 'dsa_public_key'
        self.dsa_private_key = 'dsa_private_key'

        self.mock_encrypt = patch('elgamal_message_cryptographer.ElGamalMessageCryptographer.encrypt').start()
        self.mock_encrypt.side_effect = lambda x, y: f'encrypted_{x}'

        self.mock_sign = patch('dsa_signer.DSASigner.sign').start()
        self.mock_sign.return_value = 'signature'

        self.vote = Vote(self.private_id, self.registration_id, self.candidate_id,
                         self.elgamal_public_key, self.params,
                         self.dsa_public_key, self.dsa_private_key)

    def tearDown(self):
        patch.stopall()

    def test_encrypted_private_id(self):
        self.assertEqual(self.vote.encrypted_private_id, 'encrypted_private_id')

    def test_encrypted_registration_id(self):
        self.assertEqual(self.vote.encrypted_registration_id, 'encrypted_registration_id')

    def test_encrypted_candidate_id(self):
        self.assertEqual(self.vote.encrypted_candidate_id, 'encrypted_candidate_id')

    def test_signature_private_id(self):
        self.assertEqual(self.vote.signature_private_id, 'signature')

    def test_signature_registration_id(self):
        self.assertEqual(self.vote.signature_registration_id, 'signature')

    def test_signature_candidate_id(self):
        self.assertEqual(self.vote.signature_candidate_id, 'signature')

    def test_elgamal_public_key(self):
        self.assertEqual(self.vote.elgamal_public_key, self.elgamal_public_key)

    def test_params(self):
        self.assertEqual(self.vote.params, self.params)

    def test_dsa_public_key(self):
        self.assertEqual(self.vote.dsa_public_key, self.dsa_public_key)

    def test_vote_encryption_called(self):
        self.assertTrue(self.mock_encrypt.called)
        self.assertEqual(self.mock_encrypt.call_count, 3)

    def test_vote_signing_called(self):
        self.assertTrue(self.mock_sign.called)
        self.assertEqual(self.mock_sign.call_count, 3)


if __name__ == '__main__':
    unittest.main()
