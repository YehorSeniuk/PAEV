from prime import Prime
from sympy import mod_inverse

class BlindSigner:
    @staticmethod
    def mask_message(m, public_key):
        while True:
            r = Prime.get_coprime(public_key.n)
            masked_m = (m * pow(r, public_key.e)) % public_key.n
            if True:
                return MaskedMessage(masked_m, r)

    @staticmethod
    def unmask_message(masked_m, public_key):
        r_inv = mod_inverse(masked_m.r, public_key.n)
        return (masked_m.masked_m * pow(r_inv, public_key.e)) % public_key.n

    @staticmethod
    def mask_sign(masked_m, private_key):
        return pow(masked_m.masked_m, *private_key)

    @staticmethod
    def unmask_sign(signed_masked_message, masked_m, private_key):
        return signed_masked_message * pow(masked_m.r, -1, private_key.n)

    @staticmethod
    def verify_sign(signature, m, public_key):
        return m == pow(signature, public_key.e, public_key.n)

class MaskedMessage:

    def __init__(self, masked_m, r):
        self.__masked_m = masked_m
        self.__r = r

    @property
    def masked_m(self):
        return self.__masked_m

    @property
    def r(self):
        return self.__r
