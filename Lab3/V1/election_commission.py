from dsa_signer import DSASigner
from elgamal_message_cryptographer import ElGamalMessageCryptographer

class ElectionCommission:

    def __init__(self, candidates):
        self.__registered_voters_ids = None
        self.__elgamal_key_pairs = None
        self.__voted = []
        self.__votes = {}
        self.__candidates = candidates

    @property
    def registered_voters_ids(self):
        return self.__registered_voters_ids

    @registered_voters_ids.setter
    def registered_voters_ids(self, registered_voters_ids):
        self.__registered_voters_ids = registered_voters_ids

    @property
    def elgamal_key_pairs(self):
        return self.__elgamal_key_pairs

    @elgamal_key_pairs.setter
    def elgamal_key_pairs(self, elgamal_key_pairs):
        self.__elgamal_key_pairs = elgamal_key_pairs

    def verify_vote(self, vote):
        if self.verify_signature(vote):
            voter_private_id, voter_registration_id, voter_candidate_id = self.decrypt_vote(vote)
            if voter_registration_id not in self.__voted:
                voter_candidate = self.__candidates[voter_candidate_id]
                voter_candidate.add_vote()
                self.__voted.append(voter_registration_id)
                self.__votes[voter_private_id] = voter_candidate_id
        else:
            print('Invalid signature')

    def decrypt_vote(self, vote):
        elgamal_private_key = self.__elgamal_key_pairs.get(vote.elgamal_public_key)
        if elgamal_private_key is not None:
            return (
                ElGamalMessageCryptographer.decrypt(vote.encrypted_private_id, vote.elgamal_public_key.p, elgamal_private_key),
                ElGamalMessageCryptographer.decrypt(vote.encrypted_registration_id, vote.elgamal_public_key.p, elgamal_private_key),
                ElGamalMessageCryptographer.decrypt(vote.encrypted_candidate_id, vote.elgamal_public_key.p, elgamal_private_key))
        else:
            print('Invalid key')


    def verify_signature(self, vote):
        if all((
            DSASigner.verify(str(vote.encrypted_private_id).encode(),
                            vote.signature_private_id,
                            vote.params,
                            vote.dsa_public_key),
            DSASigner.verify(str(vote.encrypted_registration_id).encode(),
                             vote.signature_registration_id,
                             vote.params,
                             vote.dsa_public_key),
            DSASigner.verify(str(vote.encrypted_candidate_id).encode(),
                             vote.signature_candidate_id,
                             vote.params,
                             vote.dsa_public_key))):
            return True
        else:
            return False

    def publish_results(self):
        for candidate_id in self.__candidates:
            print(f'Candidate ID: {candidate_id}; Votes number: {self.__candidates[candidate_id].voters_number}')
        for voter_private_id in self.__votes:
            print(f'Voter ID: {voter_private_id}; Candidate ID: {self.__votes[voter_private_id]}')