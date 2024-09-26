from dsa_signer import DSASigner
from elgamal_message_cryptographer import ElGamalMessageCryptographer

class Vote:

    def __init__(self, private_id, registration_id, candidate_id,
                 elgamal_public_key,
                 params, dsa_public_key, dsa_private_key):

        self.__encrypted_private_id = ElGamalMessageCryptographer.encrypt(private_id, elgamal_public_key)
        self.__registration_id = ElGamalMessageCryptographer.encrypt(registration_id, elgamal_public_key)
        self.__encrypted_candidate_id = ElGamalMessageCryptographer.encrypt(candidate_id, elgamal_public_key)

        self.__signature_private_id = DSASigner.sign(str(self.__encrypted_private_id).encode(), params, dsa_private_key)
        self.__signature_registration_id = DSASigner.sign(str(self.__registration_id).encode(), params, dsa_private_key)
        self.__signature_candidate_id = DSASigner.sign(str(self.__encrypted_candidate_id).encode(), params, dsa_private_key)

        # print(DSASigner.verify(str(self.__encrypted_private_id).encode(), self.__signature_private_id, params, dsa_public_key))
        self.__elgamal_public_key = elgamal_public_key
        self.__params = params
        self.__dsa_public_key = dsa_public_key

    @property
    def elgamal_public_key(self):
        return self.__elgamal_public_key
    @property
    def params(self):
        return self.__params

    @property
    def dsa_public_key(self):
        return self.__dsa_public_key

    @property
    def encrypted_private_id(self):
        return self.__encrypted_private_id

    @property
    def encrypted_registration_id(self):
        return self.__registration_id

    @property
    def encrypted_candidate_id(self):
        return self.__encrypted_candidate_id

    @property
    def signature_private_id(self):
        return self.__signature_private_id

    @property
    def signature_registration_id(self):
        return self.__signature_registration_id

    @property
    def signature_candidate_id(self):
        return self.__signature_candidate_id