import unittest
from unittest.mock import MagicMock, patch
from voter import Voter



class TestVoter(unittest.TestCase):

    def setUp(self):
        self.registration_office = MagicMock()
        self.election_commission = MagicMock()
        self.ballot = [1, 2, 3]
        self.voter = Voter(self.registration_office, self.election_commission, self.ballot)

    @patch('random.randint', return_value=150)
    def test_initialization(self, mock_randint):
        self.assertIsNotNone(self.voter._Voter__registration_office)
        self.assertIsNotNone(self.voter._Voter__election_commission)
        self.assertEqual(self.voter._Voter__ballot, self.ballot)
        self.assertIsNotNone(self.voter._Voter__private_id)
        self.assertIsNotNone(self.voter._Voter__params)
        self.assertIsNotNone(self.voter._Voter__dsa_private_key)
        self.assertIsNotNone(self.voter._Voter__dsa_public_key)
        self.assertIsNone(self.voter._Voter__registration_id)
        self.assertIsNone(self.voter._Voter__elgamal_public_key)

    @patch('random.randint', return_value=150)
    def test_register(self, mock_randint):
        self.registration_office.get_registration_id.return_value = (123, 'elgamal_public_key')

        self.voter.register()

        self.assertEqual(self.voter._Voter__registration_id, 123)
        self.assertEqual(self.voter._Voter__elgamal_public_key, 'elgamal_public_key')


    def tearDown(self):
        del self.voter


if __name__ == '__main__':
    unittest.main()
