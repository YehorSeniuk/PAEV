class ElectionCommission:

    def confirm_votes(self, votes):
        voted_registration_ids = []
        confirmed_votes = []
        for vote in votes:
            if vote.verify_signature():
                if vote.registration_id not in voted_registration_ids:
                    confirmed_votes.append(vote)
                    voted_registration_ids.append(vote.registration_id)
                else:
                    print('Already voted!')
            else:
                print('Invalid signature!')
        return confirmed_votes