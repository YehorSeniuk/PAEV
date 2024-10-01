import random
from math import gcd
import sympy

class BBSMessageCryptographer:

    @staticmethod
    def generate_primes():
        while True:
            p = sympy.randprime(300, 1000)
            if p % 4 == 3:
                break
        while True:
            q = sympy.randprime(300, 1000)
            if q % 4 == 3:
                break
        return p, q

    @staticmethod
    def generate_keys():
        p, q = BBSMessageCryptographer.generate_primes()
        n = p * q
        x = BBSMessageCryptographer.generate_x(n)
        x0 = pow(x, 2, n)
        return BBSPublicKey(n, x0), BBSPrivateKey(p, q)

    @staticmethod
    def generate_x(n):
        while True:
            x = random.randint(2, n - 1)
            if gcd(x, n) == 1:
                return x

    @staticmethod
    def bbs_generate_bits(public_key, num_bits):
        n = public_key.n
        x = public_key.x0
        bits = []
        for _ in range(num_bits):
            x = pow(x, 2, n)
            bits.append(x % 2)
        return bits

    @staticmethod
    def encrypt_integer(num, public_key):
        message_bits = BBSBits(_int=num)
        num_bits = len(message_bits)
        bits = BBSMessageCryptographer.bbs_generate_bits(public_key, num_bits)

        encrypted_bits = [(m ^ b) for m, b in zip(message_bits, bits)]
        return BBSBits(bits=encrypted_bits)

    @staticmethod
    def decrypt_integer(encrypted_bbs_bits, public_key, force_len=None):
        encrypted_bits = encrypted_bbs_bits
        num_bits = force_len or len(encrypted_bits)
        bits = BBSMessageCryptographer.bbs_generate_bits(public_key, num_bits)

        decrypted_bits = [(c ^ b) for c, b in zip(encrypted_bits, bits)]
        return BBSConverter.bits_to_int(decrypted_bits)

class BBSPublicKey:

    def __init__(self, n, x0):
        self.__n = n
        self.__x0 = x0

    @property
    def n(self):
        return self.__n

    @property
    def x0(self):
        return self.__x0

class BBSPrivateKey:

    def __init__(self, p, q):
        self.__p = p
        self.__q = q

    @property
    def p(self):
        return self.__p

    @property
    def q(self):
        return self.__q


class BBSConverter:

    @staticmethod
    def int_to_bits(num):
        return [int(bit) for bit in bin(num)[2:]]

    @staticmethod
    def bits_to_int(bits):
        return int(''.join(str(bit) for bit in bits), 2)

def mod_exp(x, e, n):
    return pow(x, e, n)

class BBSBits:

    def __init__(self, bits=None, _int=None):
        self.__bits = bits or BBSConverter.int_to_bits(_int)
        if bits is not None and _int is not None:
            assert int(self) == _int

    def __int__(self):
        return BBSConverter.bits_to_int(self.__bits)

    def __len__(self):
        return len(self.__bits)

    def __iter__(self):
        return iter(self.__bits)
