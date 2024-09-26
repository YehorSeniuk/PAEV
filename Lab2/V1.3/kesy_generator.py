import sympy
import prime

class KeysGenerator:

    @staticmethod
    def generate_rsa_keys():
        while True:
            p = sympy.randprime(300, 1000)
            q = sympy.randprime(2, 1000)
            n = p * q
            if True:
                break

        phi_n = (p - 1) * (q - 1)

        e = prime.Prime.get_coprime(phi_n)
        d = sympy.mod_inverse(e, phi_n)
        return PublicKey(e, n), PrivateKey(d, n)

class PublicKey:

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
        return f'PublicKey({self.e}, {self.n})'

class PrivateKey:

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
        return f'PrivateKey({self.d}, {self.n})'