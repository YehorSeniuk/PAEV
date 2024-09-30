from voter import Voter
from candidate import Candidate
from election_commission import ElectionCommission
from central_election_commission import CentralElectionCommission

class Protocol:

    def __init__(self):
        self.voters = None
        self.candidates = None
        self.election_commissions = None
        self.central_election_commission = None
        self.vote_pairs = []

    def start(self, voters_number, candidates_number):
        self.create_actors(voters_number, candidates_number)
        self.register_candidates_and_voters()
        self.prepare_votes()
        self.confirm_votes()
        print('=== Confirmed encoded votes ===')
        self.publish_confirmed_votes()
        self.sum_up()
        print('=== Results ===')
        self.publish_results()

    def create_actors(self, voters_number, candidates_number):
        self.voters = [Voter() for _ in range(voters_number)]
        self.candidates = [Candidate() for _ in range(candidates_number)]
        self.election_commissions = [ElectionCommission() for _ in range(2)]
        self.central_election_commission = CentralElectionCommission()

    def register_candidates_and_voters(self):
        self.central_election_commission.register_candidates(self.candidates)
        self.central_election_commission.register_voters(self.voters)

    def prepare_votes(self):
        for voter in self.voters:
            voter.prepare_vote(self.candidates, self.central_election_commission.public_encryption_key)
            self.vote_pairs.append(voter.votes)

    def confirm_votes(self):
        first_commission = self.election_commissions[0]
        second_commission = self.election_commissions[1]
        first_votes = [vote_pair[0] for vote_pair in self.vote_pairs]
        second_votes = [vote_pair[1] for vote_pair in self.vote_pairs]
        self.vote_pairs = list(zip(first_commission.confirm_votes(first_votes),
                                   second_commission.confirm_votes(second_votes)))

    def publish_confirmed_votes(self):
        for vote_pair in self.vote_pairs:
            print(vote_pair)
        print()

    def sum_up(self):
        self.central_election_commission.sum_up(self.vote_pairs, self.candidates)

    def publish_results(self):
        for vote in self.central_election_commission.votes:
            print(vote)
        for candidate in self.candidates:
            print(candidate)