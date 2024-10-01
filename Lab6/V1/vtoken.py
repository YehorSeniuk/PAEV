from elgamal_message_cryptographer import ElGamalMessageCryptographer
from bbs import BBSMessageCryptographer
class VToken:

    def __init__(self, voter_registration_id, public_elgamal_key, public_bbs_key):
        self.__voter_registration_id = voter_registration_id
        self.__public_elgamal_key = public_elgamal_key
        self.__public_bbs_key = public_bbs_key

    def encrypt(self, candidate_id):
        encrypted_candidate_id = BBSMessageCryptographer.encrypt_integer(candidate_id, self.__public_bbs_key)
        encrypted_len = ElGamalMessageCryptographer.encrypt(str(len(encrypted_candidate_id)), self.__public_elgamal_key)
        encrypted_candidate_id = ElGamalMessageCryptographer.encrypt(str(int(encrypted_candidate_id)), self.__public_elgamal_key)
        encrypted_voter_registration_id = ElGamalMessageCryptographer.encrypt(str(self.__voter_registration_id), self.__public_elgamal_key)
        return encrypted_candidate_id, encrypted_len, self.__public_bbs_key, encrypted_voter_registration_id
