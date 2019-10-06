"""
Bubble sort
average performance: O(n^2)
worst-case performance: O(n^2)
best-case performance: O(n)
"""

import unittest


def bubble_sort(a):
    """
    a: list 破壊的に更新される。
    """
    n = len(a)
    swapped = True
    while swapped:
        swapped = False
        for i in range(n - 1):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                swapped = True
        n -= 1
    return a


class TestBubbleSort(unittest.TestCase):
    def test_bubble_sort(self):
        org = [0, 4, 2]
        result = bubble_sort(org)
        self.assertEqual(result, org)

        expect = [0, 2, 4]
        self.assertEqual(result, expect)

        result = bubble_sort([1, 2, 3, 4, 5, 6, 0])
        expect = [0, 1, 2, 3, 4, 5, 6]
        self.assertEqual(result, expect)

        result = bubble_sort([1, 1, 3, -2, 5, 6, 0])
        expect = [-2, 0, 1, 1, 3, 5, 6]
        self.assertEqual(result, expect)

        result = bubble_sort([1])
        expect = [1]
        self.assertEqual(result, expect)

        result = bubble_sort(['a', 'z', 'a', 'e'])
        expect = ['a', 'a', 'e', 'z']
        self.assertEqual(result, expect)


if __name__ == '__main__':
    unittest.main()
