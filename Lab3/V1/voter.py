import random
from vote import Vote
from dsa_signer import DSASigner

class Voter:

    def __init__(self, registration_office, election_commission, ballot):
        self.__registration_office = registration_office
        self.__election_commission = election_commission
        self.__ballot = ballot
        self.__registration_id = None
        self.__private_id = str(random.randint(100, 300))
        self.__params, self.__dsa_private_key, self.__dsa_public_key,  = DSASigner.generate_params_and_keys()
        self.__elgamal_public_key = None


    def register(self):
        self.__registration_id, self.__elgamal_public_key = self.__registration_office.get_registration_id(100, 300)

    def vote(self):
        candidate_id = random.choice(self.__ballot)
        vote = Vote(self.__private_id, self.__registration_id, candidate_id,
                    self.__elgamal_public_key,
                    self.__params, self.__dsa_public_key, self.__dsa_private_key)
        self.__election_commission.verify_vote(vote)