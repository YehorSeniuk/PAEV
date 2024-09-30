import sympy
import random
import hashlib

class ElGamalSigner:

    @staticmethod
    def generate_keys():
        p = sympy.randprime(5, 1000_000)
        g = sympy.primitive_root(p)
        x = random.randrange(2, p - 2)
        y = pow(g, x, p)
        return ElGamalPublicKey(p, g, y), ElGamalPrivateKey(x)

    @staticmethod
    def hash_message(message):
        return int(hashlib.sha256(str(message).encode()).hexdigest(), 16)

    @staticmethod
    def sign_message(private_key, public_key, message):
        p = public_key.p
        g = public_key.g
        x = private_key.x

        m = ElGamalSigner.hash_message(message) % (p - 1)

        while True:
            k = random.randrange(2, p - 1)
            if sympy.gcd(k, p - 1) == 1:
                r = pow(g, k, p)
                k_inv = sympy.mod_inverse(k, p - 1)
                s = (k_inv * (m - x * r)) % (p - 1)
                if s != 0:
                    break

        return r, s

    @staticmethod
    def verify_signature(public_key, message, signature):
        p = public_key.p
        g = public_key.g
        y = public_key.y
        r, s = signature

        if not (0 < r < p and 0 < s < p - 1):
            return False

        m = ElGamalSigner.hash_message(message) % (p - 1)

        left_side = (pow(y, r, p) * pow(r, s, p)) % p
        right_side = pow(g, m, p)

        return left_side == right_side


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

    def __repr__(self):
        return f'ElGamalPrivateKey({self.x})'
