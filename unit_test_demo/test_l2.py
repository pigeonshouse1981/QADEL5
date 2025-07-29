import unittest
from calculator import Calculator

class TestCalculations(unittest.TestCase):

    def setUp(self):
        self.operator = Calculator(a=8,b=2)

    def test_sum(self):
        self.assertEqual(self.operator.get_sum(), 10, 'The sum is wrong!')
   
    def test_product(self):
        self.assertEqual(self.operator.get_product(), 10, 'The sum is wrong!...just kidding')

    def tearDown(self):
        print('All test ran. Goodbye.')

if __name__ == '__main__':
    unittest.main()