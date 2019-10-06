"""
Bogosort
average performance: O(n*n!)
worst-case performance: O(inf)
best-case performance: O(n)
"""
import random
import unittest


def bogosort(a: list) -> list:
    """
    a: list 破壊的に更新される。
    """
    n = len(a)
    while any(a[i] > a[i + 1] for i in range(n - 1)):
        random.shuffle(a)
    return a


class TestBogosort(unittest.TestCase):
    def test_bogosort(self):
        org = [0, 4, 2]
        result = bogosort(org)
        self.assertEqual(result, org)

        expect = [0, 2, 4]
        self.assertEqual(result, expect)

        result = bogosort([1, 2, 3, 4, 5, 6, 0])
        expect = [0, 1, 2, 3, 4, 5, 6]
        self.assertEqual(result, expect)

        result = bogosort([1, 1, 3, -2, 5, 6, 0])
        expect = [-2, 0, 1, 1, 3, 5, 6]
        self.assertEqual(result, expect)

        result = bogosort([1])
        expect = [1]
        self.assertEqual(result, expect)

        result = bogosort(['a', 'z', 'a', 'e'])
        expect = ['a', 'a', 'e', 'z']
        self.assertEqual(result, expect)


if __name__ == '__main__':
    unittest.main()
