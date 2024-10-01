from voter import Voter
from candidate import Candidate
from registration_office import RegistrationOffice
from election_commission import ElectionCommission

class Protocol:

    def __init__(self):
        self.voters = None
        self.candidates = None
        self.registration_office = None
        self.election_commission = None


    def start(self, voters_number, candidates_number):
        self.create_actors(voters_number, candidates_number)
        registered_voters_ids = self.registration_office.register_voters(self.voters)
        v_tokens = self.election_commission.generate_keys_for_voters(registered_voters_ids)
        self.registration_office.set_authorization_credentials(v_tokens, self.voters)
        votes = [voter.make_vote(self.candidates) for voter in self.voters]
        self.election_commission.verify_vote(votes, self.candidates)
        for candidate in self.candidates:
            print(candidate)


    def create_actors(self, voters_number, candidates_number):
        self.voters = [Voter() for _ in range(voters_number)]
        self.candidates = [Candidate(_id) for _id in range(candidates_number)]
        self.registration_office = RegistrationOffice()
        self.election_commission = ElectionCommission()
