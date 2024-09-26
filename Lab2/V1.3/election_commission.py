import random

from voter import Voter
from candidate import Candidate
from blind_signer import BlindSigner
from message_cryptographer import MessageCryptographer

class ElectionCommission:

    def __init__(self):
        self.__registered_voters = {}
        self.__registered_candidates = {}
        self.__votes = []
        self.__already_voted = []

    def register_voters(self, number):
        _ = 0
        while _ != number:
            _id = random.randint(100, 300)
            if self.__registered_voters.get(_id) is None:
                self.__registered_voters[_id] = Voter(_id, self.__registered_candidates)
                _ += 1

    def register_candidates(self, number):
        _ = 0
        while _ != number:
            _id = random.randint(100, 300)
            if self.__registered_candidates.get(_id) is None:
                self.__registered_candidates[_id] = Candidate(_id)
                _ += 1


    def start_voting(self):
        for _id in self.__registered_voters:
            voter = self.__registered_voters[_id]
            encoded_signature, encoded_message, encoded_private_id = voter.vote()
            decoded_signature = MessageCryptographer.decode_message(encoded_signature, voter.private_key)
            decoded_message = MessageCryptographer.decode_message(encoded_message, voter.private_key)
            decoded_private_id = MessageCryptographer.decode_message(encoded_private_id, voter.private_key)
            if BlindSigner.verify_sign(decoded_signature, decoded_message, voter.public_key):
                if _id not in self.__already_voted:
                    self.__votes.append((decoded_private_id, decoded_message))
                    self.__already_voted.append(_id)

    def start_sending_masked_sets(self):
        for _id in self.__registered_voters:
            voter = self.__registered_voters[_id]
            masked_kits = voter.get_masked_kits(self.__registered_candidates)
            signed_masked_kit, masked_kit = self.blind_sing(voter, masked_kits)
            voter.unmask_kit(signed_masked_kit, masked_kit)


    def count_votes(self):
        for voter_private_id, message in self.__votes:
            for candidate_id in self.__registered_candidates:
                if message == candidate_id:
                    candidate = self.__registered_candidates.get(candidate_id)
                    candidate.add_vote()

        for candidate_id in self.__registered_candidates:
            print(self.__registered_candidates[candidate_id])

        for voter_private_id, message in self.__votes:
            print(f'Voter ID: {voter_private_id}; Candidate ID: {message}')


    def _is_broken(self, kit):
        return kit != [_id for _id in self.__registered_candidates]

    def blind_sing(self, voter, masked_kits):
        random_masked_kits = random.choices(masked_kits, k=9)
        random_kits = [[BlindSigner.unmask_message(masked_message, voter.public_key) for masked_message in random_masked_kit] for random_masked_kit in random_masked_kits]
        unmasked_kit = [kit for kit in masked_kits if kit not in random_masked_kits][0]
        if all([not self._is_broken(random_kit) for random_kit in random_kits]):
            return (
                [BlindSigner.mask_sign(masked_message, voter.private_key) for masked_message in unmasked_kit],
                [masked_message for masked_message in unmasked_kit])
