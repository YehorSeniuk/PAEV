from past.builtins import reduce
import random

from dsa_signer import DSASigner
from prime import Prime

from vote import Vote

class Voter:

    def __init__(self):
        self.__registration_id = None
        self.__votes = None
        self.__params, self.__public_signature_key, self.__private_signature_key = DSASigner.generate_params_and_keys()

    @property
    def registration_id(self):
        return self.__registration_id

    @registration_id.setter
    def registration_id(self, registration_id):
        self.__registration_id = registration_id

    @property
    def votes(self):
        return self.__votes

    def prepare_vote(self, candidates, public_encryption_key):
        self.make_vote(candidates)
        self.encrypt(public_encryption_key)
        self.sign()

    def make_vote(self, candidates):
        chosen_candidate = random.choice(candidates)
        vote = Vote(chosen_candidate.registration_id, self.registration_id)
        self.__votes = self.separate(vote)

    def separate(self, vote):
        factors = Prime.factorize(vote.message)
        random.shuffle(factors)
        pivot = len(factors) // 2 if len(factors) % 2 == 0 else (len(factors) + 1) // 2
        message1, message2 = reduce(lambda a, b: a * b, factors[:pivot]), reduce(lambda a, b: a * b, factors[pivot:])
        return Vote(message1, vote.registration_id), Vote(message2, vote.registration_id)

    def encrypt(self, public_encryption_key):
        for vote in self.__votes:
            vote.encrypt(public_encryption_key)

    def sign(self):
        for vote in self.__votes:
            vote.sign(self.__params, self.__public_signature_key, self.__private_signature_key)
