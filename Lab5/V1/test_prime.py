import unittest
import sympy
from unittest.mock import patch
from prime import Prime


class TestPrime(unittest.TestCase):

    @patch('random.randint')
    def test_get_coprime(self, mock_randint):
        n = 10
        mock_randint.side_effect = [6, 7]

        coprime = Prime.get_coprime(n)
        self.assertEqual(coprime, 7)
        self.assertEqual(sympy.gcd(n, coprime), 1)

    def test_factorize(self):
        n = 18
        expected_factors = [2, 3, 3]

        result = Prime.factorize(n)
        self.assertEqual(result, expected_factors)

        n = 60
        expected_factors = [2, 2, 3, 5]

        result = Prime.factorize(n)
        self.assertEqual(result, expected_factors)


if __name__ == '__main__':
    unittest.main()
