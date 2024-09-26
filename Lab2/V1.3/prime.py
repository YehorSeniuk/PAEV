import random
from sympy import gcd


class Prime:

    @staticmethod
    def get_coprime(n):
        while True:
            candidate = random.randint(2, n - 1)
            if gcd(n, candidate) == 1:
                return candidate