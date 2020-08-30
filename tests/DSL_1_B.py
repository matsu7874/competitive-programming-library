# https://onlinejudge.u-aizu.ac.jp/courses/library/3/DSL/1/DSL_1_A


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
        # 集合の代表にリンクを繋ぎ変える
        same_group_items = []
        y = x
        while self.parent[y] >= 0:
            same_group_items.append(y)
            y = self.parent[y]
        w = 0
        while same_group_items:
            child = same_group_items.pop()
            w += self.weight[child]
            self.weight[child] = w
            self.parent[child] = y
        return y, self.weight[x]

    def unite(self, x: int, y: int, weight: int) -> bool:
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


def solve():
    n, q = map(int, input().split())
    uf = WeightedUnionFind(n)
    for _ in range(q):
        query = list(map(int, input().split()))
        if query[0] == 0:
            _, x, y, z = query
            uf.unite(x, y, z)
        else:
            _, x, y = query
            root_x, pos_x = uf.find(x)
            root_y, pos_y = uf.find(y)
            if root_x == root_y:
                print(pos_y - pos_x)
            else:
                print('?')


if __name__ == "__main__":
    solve()
