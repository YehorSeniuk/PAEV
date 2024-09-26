import unittest
from candidate import Candidate

class TestCandidate(unittest.TestCase):

    def setUp(self):
        self.candidate = Candidate(_id=1)

    def test_initial_vote_count(self):
        self.assertEqual(str(self.candidate), 'id: 1: 0')

    def test_add_vote_increases_vote_count(self):
        self.candidate.add_vote()
        self.assertEqual(str(self.candidate), 'id: 1: 1')

    def test_multiple_votes_increase_vote_count(self):
        for _ in range(3):
            self.candidate.add_vote()
        self.assertEqual(str(self.candidate), 'id: 1: 3')

    def test_str_representation(self):
        self.assertEqual(str(self.candidate), 'id: 1: 0')
        self.candidate.add_vote()
        self.assertEqual(str(self.candidate), 'id: 1: 1')

if __name__ == '__main__':
    unittest.main()
