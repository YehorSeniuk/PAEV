import random
from elgamal_message_cryptographer import ElGamalMessageCryptographer

class RegistrationOffice:

    def __init__(self, election_commission):
        self.__registered_voters_ids = []
        self.__elgamal_key_pairs = {}
        self.__election_commission = election_commission

    def get_registration_id(self, start, end):
        while True:
            new_voter_id = str(random.randint(start, end))
            if new_voter_id not in self.__registered_voters_ids:
                self.__registered_voters_ids.append(new_voter_id)
                while True:
                    elgamal_public_key, elgamal_private_key = ElGamalMessageCryptographer.generate_keys()
                    if self.__elgamal_key_pairs.get(elgamal_public_key) is None:
                        self.__elgamal_key_pairs[elgamal_public_key] = elgamal_private_key
                        return new_voter_id, elgamal_public_key

    def send_registered_voters_ids(self):
        self.__election_commission.registered_voters_ids = self.__registered_voters_ids

    def send_elgamal_key_pairs(self):
        self.__election_commission.elgamal_key_pairs = self.__elgamal_key_pairs

