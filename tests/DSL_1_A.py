# https://onlinejudge.u-aizu.ac.jp/courses/library/3/DSL/1/DSL_1_A

from snippets.data_structure.unionfind import UnionFind


def solve():
    n, q = map(int, input().split())
    uf = UnionFind(n)
    for _ in range(q):
        com, x, y = map(int, input().split())
        if com == 0:
            uf.unite(x, y)
        else:
            print(1 if uf.same(x, y) else 0)


if __name__ == "__main__":
    solve()
