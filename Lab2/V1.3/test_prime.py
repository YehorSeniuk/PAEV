import unittest
from sympy import gcd
from prime import Prime


class TestPrime(unittest.TestCase):

    def test_get_coprime(self):
        n = 10
        coprime = Prime.get_coprime(n)
        self.assertTrue(2 <= coprime < n, "Кандидат має бути між 2 і n-1")
        self.assertEqual(gcd(n, coprime), 1, "Числа повинні бути взаємно простими")

if __name__ == '__main__':
    unittest.main()
