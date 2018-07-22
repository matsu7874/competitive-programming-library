import unittest


class UnionFind:

    def __init__(self, size: int):
        # 負の値はルート (集合の代表) で集合の個数
        # 正の値は次の要素を表す
        self.size = size
        self.parent = [-1 for _ in range(size)]

    def find(self, x: int) -> int:
        """
        xを含む集合の代表を求める
        """
        if self.parent[x] < 0:
            return x
        root = self.find(self.parent[x])
        self.parent[x] = root
        return root

    def union(self, x: int, y: int):
        """
        xを含む集合とyを含む集合を併合する
        """
        s1 = self.find(x)
        s2 = self.find(y)
        if s1 != s2:
            if self.parent[s1] >= self.parent[s2]:
                self.parent[s1] += self.parent[s2]
                self.parent[s2] = s1
            else:
                self.parent[s2] += self.parent[s1]
                self.parent[s1] = s2

    def count_group(self):
        """
        集合の数を数える。
        """
        count = 0
        for i in range(self.size):
            if self.parent[i] < 0:
                count += 1
        return count


class TestUnionFind(unittest.TestCase):
    def test_union_find(self):
        n = 12
        ut = UnionFind(n)
        for i in range(n):
            self.assertEqual(ut.find(i), i)
        pairs = [(0, 1), (2, 3), (0, 2)]
        for a, b in pairs:
            ut.union(a, b)
        for a, b in pairs + [(1, 3)]:
            self.assertEqual(ut.find(a), ut.find(b))
        for i in range(4, n):
            self.assertNotEqual(ut.find(0), ut.find(i))


if __name__ == '__main__':
    unittest.main()
