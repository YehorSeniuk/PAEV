import random

from rsa_message_cryptographer import RSAMessageCryptographer

from vote import Vote

class CentralElectionCommission:

    def __init__(self):
        self.__public_encryption_key, self.__private_encryption_key = RSAMessageCryptographer.generate_keys()
        self.__votes = []

    def register_candidates(self, candidates):
        used_registration_ids =[]
        numbers = random.choices(range(10, 200), k=50)
        for candidate in candidates:
            while True:
                number1 = random.choice(numbers)
                number2 = random.choice(numbers)
                new_id = number1 * number2
                if new_id not in used_registration_ids:
                    candidate.registration_id = new_id
                    used_registration_ids.append(new_id)
                    break

    def register_voters(self, voters):
        used_registration_ids = []
        for voter in voters:
            while True:
                new_id = random.randint(1, 2 * len(voters))
                if new_id not in used_registration_ids:
                    voter.registration_id = new_id
                    used_registration_ids.append(new_id)
                    break

    def unite_votes(self, vote_pairs):
        self.__votes = [Vote(vote1.message * vote2.message,vote1.registration_id) for vote1, vote2 in vote_pairs]

    def decrypt_votes(self, votes):
        for vote in votes:
            vote.decrypt(self.__private_encryption_key)

    def count_votes(self, votes, candidates):
        for vote in votes:
            for candidate in candidates:
                if vote.message == candidate.registration_id:
                    candidate.add_vote()

    def sum_up(self, vote_pairs, candidates):
        self.unite_votes(vote_pairs)
        self.decrypt_votes(self.__votes)
        self.count_votes(self.__votes, candidates)

    @property
    def public_encryption_key(self):
        return self.__public_encryption_key

    @property
    def votes(self):
        return self.__votes
