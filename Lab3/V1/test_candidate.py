import unittest
from candidate import Candidate
class TestCandidate(unittest.TestCase):

    def setUp(self):
        self.candidate = Candidate(_id=1)

    def test_initial_votes(self):
        self.assertEqual(self.candidate.voters_number, 0)

    def test_add_vote(self):
        self.candidate.add_vote()
        self.assertEqual(self.candidate.voters_number, 1)

        self.candidate.add_vote()
        self.assertEqual(self.candidate.voters_number, 2)

    def test_id(self):
        self.assertEqual(self.candidate.id, 1)

if __name__ == '__main__':
    unittest.main()
