import unittest
from main import add_numbers
class TestMyModule(unittest.TestCase):

    def test_add_numbers(self):
        result = add_numbers(2, 3)
        self.assertEqual(result, 5, "Addition failed for 2 + 3")


if __name__ == '__main__':
    unittest.main()
