import unittest

from .example import sum


class ExampleTest(unittest.TestCase):
    def test_sum(self):
        result = sum(1, 2)
        self.assertEqual(result, 3)
