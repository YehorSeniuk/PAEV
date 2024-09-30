import random
import sympy

class Prime:

    @staticmethod
    def get_coprime(n):
        while True:
            candidate = random.randint(2, n - 1)
            if sympy.gcd(n, candidate) == 1:
                return candidate

    @staticmethod
    def factorize(n):
        factors_dict = sympy.factorint(n)
        factors = []

        for base, exponent in factors_dict.items():
            factors.extend([base] * exponent)

        return factors