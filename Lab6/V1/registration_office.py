import random

class RegistrationOffice:


    def register_voters(self, voters):
        registered_voters_ids = [registration_id for registration_id
                                    in random.sample(range(100, 300), len(voters))]
        return registered_voters_ids

    def set_authorization_credentials(self, v_tokens, voters):
        for voter, v_token in zip(voters, v_tokens):
            voter.v_token = v_token

