"""範囲に対するクエリ処理と点に対する更新処理が得意なデータ構造"""


class SegmentTree:
    """抽象的なセグメント木

    Attributes:
        n_leaf (int): 要素数以上かつ最小の2冪
        data (T): 2分木でデータを保持する
        identity (T): 単位元
        operation_function (Callable[[T, T], T]): 各ノードでの集約処理
        update_function (Callable[[T, T], None]): 各ノードでの更新処理
    """

    def __init__(self, size: int, identity, operation_function, update_function):
        """
        Args:
            size (int): 要素数
            identity (T): 単位元
            operation_function (Callable[[T, T], T]): 各ノードでの集約処理
            update_function (Callable[[T, T], None]): 各ノードでの更新処理
        Returns:
            SegmentTree
        """
        n_leaf = 1
        while n_leaf < size:
            n_leaf *= 2
        self.n_leaf = n_leaf
        self.identity = identity
        self.data = [identity] * (2 * self.n_leaf - 1)
        self.operation_function = operation_function
        self.update_function = update_function

    def _query(self, a, b, k, l, r):
        if r <= a or b <= l:
            return self.identity
        elif a <= l and r <= b:
            return self.data[k]
        else:
            m = (l+r) // 2
            child_left = self._query(a, b, 2*k+1, l, m)
            child_right = self._query(a, b, 2*k+2, m, r)
            return self.operation_function(child_left, child_right)

    def query(self, a: int, b: int):
        """半開区間[a, b)のquery結果を返す。

        Args:
            a (int): index下限(含む)
            b (int): index上限(含まない)
        Returns:
            query_result (T)
        """
        return self._query(a, b, 0, 0, self.n_leaf)

    def point_update(self, index: int, value):
        """index番目の要素を値valueで更新する。

        Args:
            index (int): 更新対象のindex
            value (T): 更新する値T
        """
        i = index + self.n_leaf - 1
        self.data[i] = self.update_function(self.data[i], value)
        while i > 0:
            i = (i - 1) // 2
            self.data[i] = self.operation_function(
                self.data[i * 2 + 1], self.data[i * 2 + 2])


class SegmentTreeRangeMinimumQuery(SegmentTree):
    """点更新の範囲最小値クエリ"""

    def __init__(self, size):
        super().__init__(
            size,
            float('inf'),
            lambda clv, crv: min(clv, crv),
            lambda org, value: value
        )


class SegmentTreeRangeSumQuery(SegmentTree):
    """点加算の範囲合計値クエリ"""

    def __init__(self, size):
        super().__init__(
            size,
            0,
            lambda clv, crv: clv + crv,
            lambda org, value: org + value
        )


if __name__ == "__main__":
    n, m = map(int, input().split())
    st = SegmentTreeRangeSumQuery(n)
    # for i in range(n):
    #     st.point_update(i, 2**31-1)
    for i in range(m):
        t, x, y = map(int, input().split())
        if t == 0:
            st.point_update(x, y)
        elif t == 1:
            print(st.query(x, y + 1))
