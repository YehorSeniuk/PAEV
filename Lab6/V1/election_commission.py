from elgamal_message_cryptographer import ElGamalMessageCryptographer
from bbs import BBSMessageCryptographer, BBSBits
from vtoken import VToken
class ElectionCommission:

    def __init__(self):
        self.__public_elgamal_key, self.__private_elgamal_key = ElGamalMessageCryptographer.generate_keys()
        self.__voter_id_bbs_keys = {}
        self.__voter_ids = None
        self.__voted_ids = []

    def generate_keys_for_voters(self, registered_voter_ids):
        v_tokens = []
        self.__voter_ids = registered_voter_ids
        for registered_voter_id in registered_voter_ids:
            bbs_public_key, bbs_private_key = BBSMessageCryptographer.generate_keys()
            self.__voter_id_bbs_keys[registered_voter_id] = (bbs_public_key, bbs_private_key)
            v_tokens.append(VToken(registered_voter_id, self.__public_elgamal_key, bbs_public_key))
        return v_tokens

    def verify_vote(self, votes, candidates):
        for vote in votes:
            decrypted_candidate_id = ElGamalMessageCryptographer.decrypt(vote.encoded_candidate_id, self.__public_elgamal_key.p, self.__private_elgamal_key)
            decrypted_len = ElGamalMessageCryptographer.decrypt(vote.encrypted_len, self.__public_elgamal_key.p,
                                                                self.__private_elgamal_key)
            decrypted_candidate_id = BBSMessageCryptographer.decrypt_integer(BBSBits(_int=int(decrypted_candidate_id)), vote.encrypted_public_key, force_len=int(decrypted_len))
            decrypted_voter_id = ElGamalMessageCryptographer.decrypt(vote.encoded_voter_id, self.__public_elgamal_key.p, self.__private_elgamal_key)
            if decrypted_voter_id not in self.__voted_ids:
                for candidate in candidates:
                    if candidate.registration_id == decrypted_candidate_id:
                        candidate.add_vote()
                self.__voted_ids.append(decrypted_voter_id)
