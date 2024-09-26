from election_commission import ElectionCommission

class Protocol:

    @staticmethod
    def start_simulation(voters_number, candidate_number):
        election_commission = ElectionCommission()
        election_commission.register_candidates(candidate_number)
        election_commission.register_voters(voters_number)
        election_commission.start_sending_masked_sets()
        election_commission.start_voting()
        election_commission.count_votes()
