import unittest


class UnionFind:

    def __init__(self, size: int):
        # 負の値はルート (集合の代表) で集合の個数
        # 正の値は次の要素を表す
        self.size = size
        self.parent = [-1] * size

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
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x != root_y:
            if self.parent[root_x] >= self.parent[root_y]:
                self.parent[root_x] += self.parent[root_y]
                self.parent[root_y] = root_x
            else:
                self.parent[root_y] += self.parent[root_x]
                self.parent[root_x] = root_y

    def count_group(self):
        """
        集合の数を数える。
        """
        count = 0
        for i in range(self.size):
            if self.parent[i] < 0:
                count += 1
        return count


class WeightedUnionFind:
    """
    重み付きUnionFind

    """
    root_position = 0

    def __init__(self, size: int):
        self.size = size
        # 負の値はルート (集合の代表) で集合の個数
        # 正の値は次の要素を表す
        self.parent = [-1] * size
        self.weight = [WeightedUnionFind.root_position] * size

    def find(self, x: int) -> (int, int):
        """
        xを含む集合の代表とxの代表からの位置を求める
        """
        if self.parent[x] < 0:
            return x, self.weight[x]
        root, weight = self.find(self.parent[x])
        self.parent[x] = root
        self.weight[x] += weight
        return root, self.weight[x]

    def union(self, x: int, y: int, weight: int) -> bool:
        """
        xを含む集合とyを含む集合を併合する
        `weight[x] + weight = weight[y]`になるように辺に重みをもたせる。
        xとyがすでに同じ集合に含まれている場合Falseを返す。
        """
        root_x, weight_x = self.find(x)
        root_y, weight_y = self.find(y)

        if root_x == root_y:
            return False

        if self.parent[root_x] >= self.parent[root_y]:
            self.parent[root_x] += self.parent[root_y]
            self.parent[root_y] = root_x
            self.weight[root_y] = weight_x + weight - weight_y
        else:
            self.parent[root_y] += self.parent[root_x]
            self.parent[root_x] = root_y
            self.weight[root_x] = weight_y - weight - weight_x

        return True


class TestUnionFind(unittest.TestCase):
    def test_init(self):
        n = 12
        ut = UnionFind(n)
        for i in range(n):
            self.assertEqual(ut.find(i), i)

    def test_union_find(self):
        n = 12
        ut = UnionFind(n)
        pairs = [(0, 1), (2, 3), (0, 2)]
        for x, y in pairs:
            ut.union(x, y)
        for x, y in pairs + [(1, 3)]:
            self.assertEqual(ut.find(x), ut.find(y))
        for i in range(4, n):
            self.assertNotEqual(ut.find(0), ut.find(i))


class TestWeightedUnionFind(unittest.TestCase):
    def test_init(self):
        n = 3
        wut = WeightedUnionFind(n)
        for i in range(n):
            self.assertEqual(wut.find(i), (i, WeightedUnionFind.root_position))

    def test_union_find(self):
        n = 3
        wut = WeightedUnionFind(n)
        pairs = [(0, 1, 1), (1, 2, 1)]
        for x, y, w in pairs:
            wut.union(x, y, w)

        expected_weight = [0, 1, 2]
        for i in range(n):
            expected = (wut.find(0)[0], wut.find(0)[1] + expected_weight[i])
            self.assertEqual(expected, wut.find(i))


if __name__ == '__main__':
    unittest.main()
