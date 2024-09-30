import unittest
from sympy import gcd
from prime import Prime

class TestPrime(unittest.TestCase):

    def test_get_coprime_basic(self):
        n = 100
        coprime = Prime.get_coprime(n)
        self.assertEqual(gcd(n, coprime), 1, f"{coprime} не є взаємно простим з {n}")

    def test_get_coprime_large_n(self):
        n = 1000000
        coprime = Prime.get_coprime(n)
        self.assertEqual(gcd(n, coprime), 1, f"{coprime} не є взаємно простим з {n}")

    def test_get_coprime_prime_n(self):
        n = 997
        coprime = Prime.get_coprime(n)
        self.assertEqual(gcd(n, coprime), 1, f"{coprime} не є взаємно простим з {n}")

    def test_get_coprime_edge_case_n_equals_2(self):
        n = 2
        with self.assertRaises(ValueError):
            Prime.get_coprime(n)

    def test_get_coprime_multiple_calls(self):
        n = 100
        coprimes = {Prime.get_coprime(n) for _ in range(10)}
        self.assertTrue(len(coprimes) > 1, "Всі числа однакові, хоча мають бути різними")

    def test_get_coprime_n_equals_1(self):
        n = 1
        with self.assertRaises(ValueError):
            Prime.get_coprime(n)

if __name__ == '__main__':
    unittest.main()
