import unittest
from calculator import Calculator

class TestOperations(unittest.TestCase):

    def test_sum(self):
        testCal = Calculator(8,2)
        self.assertEqual(testCal.get_sum(), 10, "incorrect")


if __name__ == "__main__":
    unittest.main()