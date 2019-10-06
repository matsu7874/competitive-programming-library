"""
BIT, Fenwick Tree

* [フェニック木(Binary Indexed Tree) - FreeStyleWiki](https://freestylewiki.xyz/fswiki/wiki.cgi?page=%E3%83%95%E3%82%A7%E3%83%8B%E3%83%83%E3%82%AF%E6%9C%A8%28Binary+Indexed+Tree%29)
* [Binary indexed tree](https://www.slideshare.net/hcpc_hokudai/binary-indexed-tree)
* [Binary Indexed Tree のはなし](http://hos.ac/slides/20140319_bit.pdf)
"""
import unittest


class BinaryIndexedTree:
    """
    0-indexed
    """

    def __init__(self, size: int, init_value: int = 0):
        self.size = size
        self.bit = [init_value] * size
        for idx in range(size):
            if idx | (idx+1) < size:
                self.bit[idx | (idx+1)] += self.bit[idx]

    def add(self, idx, value):
        while idx < self.size:
            self.bit[idx] += value
            idx |= idx+1

    def _sum(self, r):
        """
        [0, r) の合計値を返却する
        """
        ret = 0
        idx = r-1
        while idx >= 0:
            ret += self.bit[idx]
            idx = (idx & (idx+1)) - 1
        return ret

    def sum(self, l, r):
        """
        [l, r) の合計値を返却する
        """
        return self._sum(r) - self._sum(l)


class TestUnionFind(unittest.TestCase):
    def test_init(self):
        bit = BinaryIndexedTree(0)
        self.assertEqual(bit.bit, [])

        n = 17
        bit = BinaryIndexedTree(n)
        self.assertEqual(bit.bit, [0] * n)

        bit = BinaryIndexedTree(16, 1)
        self.assertEqual(bit.bit, [1, 2, 1, 4, 1, 2,
                                   1, 8, 1, 2, 1, 4, 1, 2, 1, 16])

        bit = BinaryIndexedTree(12, -1)
        self.assertEqual(
            bit.bit, [-1, -2, -1, -4, -1, -2, -1, -8, -1, -2, -1, -4])

    def test_add(self):
        n = 12
        bit = BinaryIndexedTree(n)
        for i in range(n):
            bit.add(i, 1)
        self.assertEqual(bit.bit, [1, 2, 1, 4, 1, 2, 1, 8, 1, 2, 1, 4])
        for i in range(n):
            bit.add(i, 1)
        self.assertEqual(bit.bit, [2, 4, 2, 8, 2, 4, 2, 16, 2, 4, 2, 8])

    def test_sum(self):
        n = 12
        bit = BinaryIndexedTree(n, 1)
        self.assertEqual(bit._sum(0), 0)
        self.assertEqual(bit._sum(1), 1)
        self.assertEqual(bit._sum(4), 4)
        self.assertEqual(bit.sum(0, 12), 12)
        self.assertEqual(bit.sum(0, 12), 12)


if __name__ == '__main__':
    unittest.main()
