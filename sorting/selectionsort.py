"""
Selection sort
average performance: O(n^2)
worst-case performance: O(n^2)
best-case performance: O(n^2)
"""

import unittest


def selection_sort(a):
    """
    a: list 破壊的に更新される。
    """
    n = len(a)
    for i in range(n - 1):
        min_i = i
        for j in range(i + 1, n):
            if a[j] < a[min_i]:
                min_i = j
        if min_i > i:
            a[i], a[min_i] = a[min_i], a[i]
    return a


class TestSelectionSort(unittest.TestCase):
    def test_selection_sort(self):
        org = [0, 4, 2]
        result = selection_sort(org)
        self.assertEqual(result, org)

        expect = [0, 2, 4]
        self.assertEqual(result, expect)

        result = selection_sort([1, 2, 3, 4, 5, 6, 0])
        expect = [0, 1, 2, 3, 4, 5, 6]
        self.assertEqual(result, expect)

        result = selection_sort([1, 1, 3, -2, 5, 6, 0])
        expect = [-2, 0, 1, 1, 3, 5, 6]
        self.assertEqual(result, expect)

        result = selection_sort([1])
        expect = [1]
        self.assertEqual(result, expect)

        result = selection_sort(['a', 'z', 'a', 'e'])
        expect = ['a', 'a', 'e', 'z']
        self.assertEqual(result, expect)


if __name__ == '__main__':
    unittest.main()
