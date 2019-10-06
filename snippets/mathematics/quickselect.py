"""
median of medians
average performance: O(n)
worst-case performance: O(n)
best-case performance: O(n)
"""

import unittest


def select(array, left, right, n):
    while left < right:
        pivot_index = get_pivot(array, left, right)
        pivot_index = partition(array, left, right, pivot_index, n)
        if n == pivot_index:
            return pivot_index
        elif n < pivot_index:
            right = pivot_index - 1
        else:
            left = pivot_index + 1
    return left


def get_pivot(array, left, right):
    if right - left < 5:
        return partition5(array, left, right)
    for i in range(left, right, 5):
        sub_right = 4
        if sub_right > right:
            sub_right = right
        median5 = partition5(array, i, sub_right)
        array[median5], array[left +
                              (i-left)//5] = array[left + (i-left)//5], array[median5]
    mid = (right - left) / 10 + left + 1
    return select(array, left, left + (right - left)//5, mid)


def partition5(array, left, right):
    i = left + 1
    while i <= right:
        j = i
        while j > left and array[j-1] > array[j]:
            array[j-1], array[j] = array[j], array[j-1]
            j = j-1
        i = i+1
    return (left+right)//2


def partition(array, left, right, pivot_index, n):
    pivot_value = array[pivot_index]
    array[pivot_index], array[right] = array[right], array[pivot_index]
    store_index = left

    for i in range(left, right):
        if array[i] < pivot_value:
            array[store_index], array[i] = array[i], array[store_index]
            store_index += 1
    store_index_eq = store_index
    for i in range(store_index, right):
        if array[i] == pivot_value:
            array[store_index_eq], array[i] = array[i], array[store_index_eq]
            store_index_eq += 1
    if n < store_index:
        return store_index
    if n <= store_index_eq:
        return n
    return store_index_eq


class TestMedianOfMedians(unittest.TestCase):
    def test_median_of_medians(self):
        pass


if __name__ == '__main__':
    unittest.main()
