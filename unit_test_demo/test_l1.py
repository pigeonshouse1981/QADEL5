import unittest
from calculator import Calculator

class TestOperations(unittest.TestCase):

    def test_sum(self):
        calculation = Calculator(2,2)
        answer = calculation.get_sum()
        self.assertEqual(answer, 4, 'The sum is wrong. ')


    def test_difference(self):
        calculation = Calculator(6,2)
        answer = calculation.get_difference()
        self.assertEqual(answer, 4, 'The sum is wrong. ')

    def test_product(self):
        calculation = Calculator(6,2)
        answer = calculation.get_product()
        self.assertEqual(answer, 12, 'The sum is wrong. ')

    def test_quotient(self):
        calculation = Calculator(6,2)
        answer = calculation.get_quotient()
        self.assertEqual(answer, 3, 'The sum is wrong. ')


if __name__ == '__main__':
    unittest.main()