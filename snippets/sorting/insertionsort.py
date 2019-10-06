"""
Insertion sort
average performance: O(n^2)
worst-case performance: O(n^2)
best-case performance: O(n)
"""

import unittest


def insertion_sort(a):
    """
    a: list 破壊的に更新される。
    """
    n = len(a)
    for i in range(1, n):
        t = a[i]
        if a[i - 1] > t:
            j = i
            while (j > 0 and a[j - 1] > t):
                a[j] = a[j - 1]
                j -= 1
            a[j] = t
    return a


class TestInsertionSort(unittest.TestCase):
    def test_insertion_sort(self):
        org = [0, 4, 2]
        result = insertion_sort(org)
        self.assertEqual(result, org)

        expect = [0, 2, 4]
        self.assertEqual(result, expect)

        result = insertion_sort([1, 2, 3, 4, 5, 6, 0])
        expect = [0, 1, 2, 3, 4, 5, 6]
        self.assertEqual(result, expect)

        result = insertion_sort([1, 1, 3, -2, 5, 6, 0])
        expect = [-2, 0, 1, 1, 3, 5, 6]
        self.assertEqual(result, expect)

        result = insertion_sort([1])
        expect = [1]
        self.assertEqual(result, expect)

        result = insertion_sort(['a', 'z', 'a', 'e'])
        expect = ['a', 'a', 'e', 'z']
        self.assertEqual(result, expect)


if __name__ == '__main__':
    unittest.main()
