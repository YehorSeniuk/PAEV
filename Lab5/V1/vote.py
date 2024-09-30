from rsa_message_cryptographer import RSAMessageCryptographer
from dsa_signer import DSASigner

class Vote:

    def __init__(self, candidate_id, registration_id):
        self.__message = candidate_id
        self.__registration_id = registration_id
        self.__signature = None
        self.__params = None
        self.__public_signature_key = None

    @property
    def message(self):
        return self.__message

    @property
    def registration_id(self):
        return self.__registration_id

    def encrypt(self, public_encryption_key):
        self.__message = RSAMessageCryptographer.encode_message(self.__message, public_encryption_key)

    def decrypt(self, private_encryption_key):
        self.__message = RSAMessageCryptographer.decode_message(self.__message, private_encryption_key)

    def sign(self, params, public_signature_key, private_signature_key):
        self.__params = params
        self.__public_signature_key = public_signature_key
        self.__signature = DSASigner.sign(self.__message, self.__params, private_signature_key)

    def verify_signature(self):
        return DSASigner.verify(self.__message, self.__signature, self.__params, self.__public_signature_key.y)

    def __repr__(self):
        return f'Voter ID:{self.registration_id}; Candidate ID: {self.__message}'