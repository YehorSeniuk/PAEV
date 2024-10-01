from copy import deepcopy
from random import randrange
from sympy import isprime
from sympy.ntheory.residue_ntheory import primitive_root

class ElGamalMessageCryptographer:

    @staticmethod
    def generate_keys():
        p = ElGamalMessageCryptographer.generate_prime(1000)
        g = primitive_root(p)
        x = randrange(2, p - 2)
        y = pow(g, x, p)
        return ElGamalPublicKey(p, g, y), ElGamalPrivateKey(x)

    @staticmethod
    def generate_prime(limit=1000):
        while True:
            p = randrange(137, limit, 2)
            if isprime(p):
                return p

    @staticmethod
    def encrypt(message, public_key):
        blocks = [ord(char) for char in message]
        cipher_pairs = []
        k = randrange(2, public_key.p - 1)

        for m in blocks:
            a = pow(public_key.g, k, public_key.p)
            b = (m * pow(public_key.y, k, public_key.p)) % public_key.p
            cipher_pairs.append((a, b))

        return CipherPairs(cipher_pairs)

    @staticmethod
    def decrypt(cipher_pairs, p, x):
        decrypted_message = []

        for a, b in cipher_pairs:
            s = pow(a, p - 1 - x, p)
            m = (b * s) % p
            decrypted_message.append(chr(m))

        return ''.join(decrypted_message)

class ElGamalPublicKey:

    def __init__(self, p, g, y):
        self.__p = p
        self.__g = g
        self.__y = y

    @property
    def p(self):
        return self.__p

    @property
    def g(self):
        return self.__g

    @property
    def  y(self):
        return self.__y

    def __repr__(self):
        return f'ElGamalPublicKey({self.p}, {self.g}, {self.y})'

class ElGamalPrivateKey:

    def __init__(self, x):
        self.__x = x

    @property
    def x(self):
        return self.__x

    def __add__(self, other):
        return self.x + other

    def __radd__(self, other):
        return self + other

    def __mul__(self, other):
        return self.x * other

    def __rmul__(self, other):
        return self * other

    def __mod__(self, other):
        return self.x % other

    def __rmod__(self, other):
        return self * other

    def __pow__(self, power, modulo=None):
        return pow(self.x, power, modulo)

    def __sub__(self, other):
        return self.x - other

    def __rsub__(self, other):
        return other - self.x

    def __repr__(self):
        return f'ElGamalPrivateKey({self.x})'

class CipherPairs:

    def __init__(self, cipher_pairs):
        self.__cipher_pairs = cipher_pairs

    @property
    def cipher_pairs(self):
        return deepcopy(self.__cipher_pairs)

    def __iter__(self):
        return iter(self.cipher_pairs)

    def __repr__(self):
        return f'{[block for block in self]}'