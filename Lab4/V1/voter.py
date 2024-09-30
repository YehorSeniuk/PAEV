import random

from rsa_message_cryptographer import RSAMessageCryptographer
from elgamal_signer import ElGamalSigner

from vote import Vote

class Voter:

    def __init__(self, candidates):
        self.__public_encryption_key, self.__private_encryption_key = RSAMessageCryptographer.generate_keys()
        self.__public_signature_key, self.__private_signature_key = ElGamalSigner.generate_keys()
        self.__candidates = candidates
        self.__private_id = random.randint(100 , 300)
        self.__vote = None

    def make_vote(self):
        candidate = random.choice(self.__candidates)
        candidate_id = candidate.id
        self.__vote = Vote(candidate_id, self.__private_id)

    def add_interference(self, public_encryption_key):
       self.__vote.add_interference(public_encryption_key)


    def encrypt(self, public_encryption_key):
        self.__vote.encrypt(public_encryption_key)

    def decrypt(self, vote):
        vote.decrypt(self.__private_encryption_key)
        return vote

    def remove_interference(self, vote):
        vote.remove_interference(self.__private_encryption_key)
        return vote

    def own_vote_exists(self, all_votes):
        for vote in all_votes:
            if vote.private_id == self.__private_id:
                return True
        else:
            return False

    def sign(self, vote):
        vote.sign(self.__public_signature_key, self.__private_signature_key)
        return vote

    def verify_signature(self, vote, public_signature_key):
        return vote.verify_signature(public_signature_key)

    @property
    def public_encryption_key(self):
        return self.__public_encryption_key

    @property
    def public_signature_key(self):
        return self.__public_signature_key

    @property
    def private_id(self):
        return self.__private_id

    @property
    def vote(self):
        return self.__vote