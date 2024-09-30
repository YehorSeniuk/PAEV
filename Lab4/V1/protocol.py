import random
from voter import Voter
from candidate import Candidate
class Protocol:

    def __init__(self, voters_number, candidates_number):
        self.__candidates = [Candidate(_id) for _id in range(1, candidates_number + 1)]
        self.__registered_voters = [Voter(self.__candidates) for _ in range(voters_number)]

    def vote(self):
        for voter in self.__registered_voters:
            voter.make_vote()

    def add_interference(self):
        for voter in self.__registered_voters:
            voter.add_interference(voter.public_encryption_key)

    def encrypt(self):
        for voter_i in self.__registered_voters[::-1]:
            for voter_j in self.__registered_voters:
                voter_j.encrypt(voter_i.public_encryption_key)

    def add_interference_and_encrypt(self):
        for voter_i in self.__registered_voters[::-1]:
            for voter_j in self.__registered_voters:
                voter_j.add_interference(voter_i.public_encryption_key)
                voter_j.encrypt(voter_i.public_encryption_key)

    def decrypt(self):
        current_votes = [voter.vote for voter in self.__registered_voters]
        random.shuffle(current_votes)
        for voter in self.__registered_voters:
            decrypted_votes = [voter.decrypt(vote) for vote in current_votes]
            current_votes = [voter.remove_interference(vote) for vote in decrypted_votes]
            if not voter.own_vote_exists(current_votes):
                print('Vote is stollen!')

    def decrypt_and_sign(self):
        current_votes = [voter.vote for voter in self.__registered_voters]
        random.shuffle(current_votes)
        for voter in self.__registered_voters:

            if voter != self.__registered_voters[0]:
                prev_voter = self.__registered_voters[self.__registered_voters.index(voter) - 1]
                for vote in current_votes:
                   if not voter.verify_signature(vote, prev_voter.public_signature_key):
                       print('Invalid signature!')

            decrypted_votes = [voter.decrypt(vote) for vote in current_votes]

            if not voter.own_vote_exists(decrypted_votes):
                print('Vote is stollen!')

            current_votes = [voter.sign(vote) for vote in decrypted_votes]

        last_voter = self.__registered_voters[-1]
        for voter in self.__registered_voters:
            for vote in current_votes:
                if not voter.verify_signature(vote, last_voter.public_signature_key):
                    print('Last signature is invalid!')

        current_votes = [voter.remove_interference(vote) for vote in current_votes for voter in self.__registered_voters if voter.vote == vote]

        for vote in current_votes:
            for candidate in self.__candidates:
                if candidate.id == vote.message:
                    candidate.add_vote()
                    print(f'Voter ID: {vote.private_id}; Candidate ID: {candidate.id}')

        for candidate in self.__candidates:
            print(candidate)

    def start(self):
        self.vote()
        self.add_interference()
        self.encrypt()
        self.add_interference_and_encrypt()
        self.decrypt()
        self.decrypt_and_sign()

