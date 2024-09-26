from election_commission import ElectionCommission
from registration_office import RegistrationOffice
from voter import Voter
from candidate import Candidate
import random

class Protocol:

    def __init__(self):
        self.__voters = None
        self.__candidates = None
        self.__registration_office = None
        self.__election_commission = None
        self.__ballot = None

    def start(self, voters_number, candidates_number):
        self.create_actors(voters_number, candidates_number)
        self.register_candidates(candidates_number)
        self.register_voters()
        self.send_registered_voters_and_keys()
        self.start_voting()
        self.count_votes()
        self.publish_results()

    def create_actors(self, voters_number, candidates_number):
        self.__candidates, self.__ballot = self.register_candidates(candidates_number)
        self.__election_commission = ElectionCommission(self.__candidates)
        self.__registration_office = RegistrationOffice(self.__election_commission)
        self.__voters = [Voter(self.__registration_office, self.__election_commission, self.__ballot) for _ in range(voters_number)]

    def register_candidates(self, candidates_number):
        candidates = {}
        ballot = []
        _ = 0
        while _ != candidates_number:
            new_candidate_id = str(random.randint(100, 300))
            if candidates.get(new_candidate_id) is None:
                candidates[new_candidate_id] = Candidate(new_candidate_id)
                ballot.append(new_candidate_id)
                _ += 1
        return candidates, ballot

    def register_voters(self):
        for voter in self.__voters:
            voter.register()

    def send_registered_voters_and_keys(self):
        self.__registration_office.send_registered_voters_ids()
        self.__registration_office.send_elgamal_key_pairs()

    def start_voting(self):
        for voter in self.__voters:
            voter.vote()

    def count_votes(self):
        pass

    def publish_results(self):
        self.__election_commission.publish_results()


