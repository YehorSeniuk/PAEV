import unittest
from crypto import generate_rsa_keys, vote, count_votes, xor_cipher
import random


class TestVotingSystem(unittest.TestCase):

    def setUp(self):
        self.candidates = ['Кандидат_А', 'Кандидат_Б']
        self.cvk_pub_key, self.cvk_priv_key = generate_rsa_keys()
        self.voters = {f'voter_{i + 1}': generate_rsa_keys() for i in range(4)}
        self.registered_voters = set(self.voters.keys())
        self.voted = set()
        self.votes = []

    def test_no_rights_to_vote(self):
        with self.assertRaises(KeyError):
            vote('invalid_voter', self.candidates[0], self.cvk_priv_key, self.cvk_pub_key,
                 self.registered_voters, self.voted)

    def test_double_voting(self):
        voter = 'voter_1'
        vote(voter, self.candidates[0], self.cvk_priv_key, self.cvk_pub_key,
             self.registered_voters, self.voted)
        with self.assertRaises(ValueError):
            vote(voter, self.candidates[0], self.cvk_priv_key, self.cvk_pub_key,
                 self.registered_voters, self.voted)

    def test_confidentiality(self):
        for voter in self.voters.keys():
            candidate = random.choice(self.candidates)
            encrypted_vote, signature, key = vote(voter, candidate, self.cvk_priv_key, self.cvk_pub_key,
                                                  self.registered_voters, self.voted)
            self.votes.append((encrypted_vote, signature, key))

        for encrypted_vote, signature, key in self.votes:
            decrypted_vote = xor_cipher(encrypted_vote, key)
            self.assertIn(decrypted_vote, self.candidates)

    def test_vote_counting(self):
        for voter in self.voters.keys():
            candidate = random.choice(self.candidates)
            encrypted_vote, signature, key = vote(voter, candidate, self.cvk_priv_key, self.cvk_pub_key,
                                                  self.registered_voters, self.voted)
            self.votes.append((encrypted_vote, signature, key))

        results = count_votes(self.votes, self.cvk_priv_key, self.cvk_pub_key, self.candidates)

        for candidate in self.candidates:
            expected_count = sum(1 for enc_vote, sig, key in self.votes if xor_cipher(enc_vote, key) == candidate)
            self.assertEqual(results.get(candidate, 0), expected_count)




