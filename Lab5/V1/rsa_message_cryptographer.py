import sympy
from prime import Prime

class RSAMessageCryptographer:

    @staticmethod
    def generate_keys():
        while True:
            p = 881
            q = 947
            n = p * q
            if p != q:
                break

        phi_n = (p - 1) * (q - 1)

        e = Prime.get_coprime(phi_n)
        d = int(sympy.mod_inverse(e, phi_n))

        return RSAPublicKey(e, n), RSAPrivateKey(d, n)

    @staticmethod
    def encode_message(m, public_key):
        return pow(m, *public_key)

    @staticmethod
    def decode_message(c, private_key):
        return  pow(c, *private_key)

class RSAPublicKey:

    def __init__(self, e, n):
        self.__e = e
        self.__n = n

    @property
    def e(self):
        return self.__e

    @property
    def n(self):
        return self.__n

    def __iter__(self):
        return iter((self.e, self.n))

    def __str__(self):
        return f'RSAPublicKey({self.e}, {self.n})'

class RSAPrivateKey:

    def __init__(self, d, n):
        self.__d = d
        self.__n = n

    @property
    def d(self):
        return self.__d

    @property
    def n(self):
        return self.__n

    def __iter__(self):
        return iter((self.d, self.n))

    def __str__(self):
        return f'RSAPrivateKey({self.d}, {self.n})'