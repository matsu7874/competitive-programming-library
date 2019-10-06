"""
Quicksort
average performance: O(n log n)
worst-case performance: O(n^2)
best-case performance: O(n log n)
"""

import unittest


def quicksort(a):
    """
    a: list
    """
    n = len(a)
    if n <= 1:
        return a
    pivot = a[0]
    left = []
    right = []
    for x in a[1:]:
        if x <= pivot:
            left.append(x)
        else:
            right.append(x)
    left = quicksort(left)
    right = quicksort(right)
    return left + [pivot] + right


class TestQuicksort(unittest.TestCase):
    def test_quicksort(self):
        org = [0, 4, 2]
        result = quicksort(org)
        expect = [0, 2, 4]
        self.assertEqual(result, expect)

        result = quicksort([1, 2, 3, 4, 5, 6, 0])
        expect = [0, 1, 2, 3, 4, 5, 6]
        self.assertEqual(result, expect)

        result = quicksort([1, 1, 3, -2, 5, 6, 0])
        expect = [-2, 0, 1, 1, 3, 5, 6]
        self.assertEqual(result, expect)

        result = quicksort([1])
        expect = [1]
        self.assertEqual(result, expect)

        result = quicksort(['a', 'z', 'a', 'e'])
        expect = ['a', 'a', 'e', 'z']
        self.assertEqual(result, expect)


if __name__ == '__main__':
    unittest.main()
