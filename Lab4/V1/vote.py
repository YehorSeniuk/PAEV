import random

from rsa_message_cryptographer import RSAMessageCryptographer
from elgamal_signer import ElGamalSigner

class Vote:

    def __init__(self, candidate_id, private_id):
        self.__message = candidate_id
        self.__private_id = private_id
        self.__signature = None
        self.__interferences = []
        self.encryption_level = 0

    def encrypt(self, public_encryption_key):
        self.__message = RSAMessageCryptographer.encode_message(self.__message, public_encryption_key)
        self.encryption_level += 1

    def decrypt(self, private_encryption_key):
        self.__message = RSAMessageCryptographer.decode_message(self.__message, private_encryption_key)
        self.encryption_level -= 1

    def sign(self, public_signature_key, private_signature_key):
        self.__signature = ElGamalSigner.sign_message(private_signature_key, public_signature_key, self.__message)

    def verify_signature(self, public_signature_key):
        return ElGamalSigner.verify_signature(public_signature_key, self.__message, self.__signature)

    def add_interference(self, public_encryption_key):
        interference = random.randint( 100, 400)
        encoded_interference = RSAMessageCryptographer.encode_message(interference, public_encryption_key)
        self.__interferences.append(encoded_interference)
        self.__message  += interference

    def remove_interference(self, private_encryption_key):
        encoded_interference = self.__interferences.pop(-1)
        decoded_interference = RSAMessageCryptographer.decode_message(encoded_interference, private_encryption_key)
        self.__message  -= decoded_interference

    @property
    def private_id(self):
        return self.__private_id

    def __repr__(self):
        return f'Voter ID: {self.__private_id}; Candidate ID: {self.__message}; EL: {self.encryption_level}'

    @property
    def message(self):
        return self.__message