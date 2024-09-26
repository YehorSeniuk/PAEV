from kesy_generator import KeysGenerator
from blind_signer import BlindSigner
from message_cryptographer import MessageCryptographer
import random

class Voter:

    def __init__(self, _id, candidates):
        self.__id = _id
        self.__private_id = random.randint(100, 1000)
        self.__public_key, self.__private_key = KeysGenerator.generate_rsa_keys()
        self.__signed_kit= []
        self.candidates = [candidate_id for candidate_id in candidates]

    def get_masked_kits(self, candidates):
        return [[BlindSigner.mask_message(_id, self.public_key) for _id in candidates] for _ in range(10)]


    def unmask_kit(self, signed_masked_kit, masked_kit):
        self.__signed_kit = list(zip([BlindSigner.unmask_sign(signed_masked_message, masked_message, self.public_key)
                                      for signed_masked_message, masked_message in zip(signed_masked_kit, masked_kit)], self.candidates))

    def vote(self):
        signature, message = random.choice(self.__signed_kit)
        encoded_signature = MessageCryptographer.encode_message(signature, self.public_key)
        encoded_message = MessageCryptographer.encode_message(message, self.public_key)
        encoded_private_id = MessageCryptographer.encode_message(self.__private_id, self.public_key)
        return encoded_signature, encoded_message, encoded_private_id

    @property
    def public_key(self):
        return self.__public_key

    @property
    def private_key(self):
        return self.__private_key

