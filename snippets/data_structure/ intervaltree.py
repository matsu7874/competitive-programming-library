"""範囲に対するクエリ処理と点に対する更新処理が得意なデータ構造"""
import unittest


class SegmentTree:
    """抽象的なセグメント木

    Attributes:
        n_leaf (int): 要素数以上かつ最小の2冪
        data (T): 2分木でデータを保持する
        data_identity (T): モノイドの単位元
        operation_identity (T): 作用素の単位元
        operation_function (Callable[[T, T], T]): 各ノードでの集約処理
        update_function (Callable[[T, U, int], T]): 各ノードでの更新処理
        propagate_function (Callable[[U, U], U]): 各ノードでの更新処理
    """

    def __init__(
        self,
        size: int,
        data_identity,
        operation_identity,
        operation_function,
        update_function,
        propagate_function,
    ):
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
        self.data_identity = data_identity
        self.operation_identity = operation_identity
        self.data = [data_identity] * (2 * self.n_leaf - 1)
        self.lazy = [operation_identity] * (2 * self.n_leaf - 1)
        self.operation_function = operation_function
        self.update_function = update_function
        self.propagate_function = propagate_function

    def _query(self, a, b, k, l, r):
        if r <= a or b <= l:
            return self.data_identity
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

    def point_set(self, index: int, value):
        i = index + self.n_leaf - 1
        self.data[i] = self.update_function(self.data[i], value)

    def build(self):
        """point_setした値を上位ノードに伝播する"""
        for i in range(self.n_leaf - 2, -1, -1):
            self.data[i] = self.operation_function(
                self.data[i * 2 + 1], self.data[i * 2 + 2])

    def point_update(self, index: int, value):
        """index番目の要素を値valueで更新する。

        Args:
            index (int): 更新対象のindex
            value (T): 更新する値T
        """
        self.point_set(index, value)
        self.build()

    def propagate(self, index: int, len: int):
        if self.lazy[index] == self.operation_identity:
            return None  # 更新の必要なし
        if index < self.n_leaf-1:
            self.lazy[2*index+1] = self.propagate_function(
                self.lazy[index], self.lazy[2*index + 1])
            self.lazy[2*index+2] = self.propagate_function(
                self.lazy[index], self.lazy[2*index + 2])
        self.data[index] = self.update_function(
            self.data[index], self.lazy[index], len)
        self.lazy[index] = self.operation_identity

    def _update(self, a, b, x, k, l, r):
        self.propagate(k, r - l)
        if r <= a or b <= l:
            return self.data[k]
        elif a <= l and r <= b:
            self.lazy[k] = self.propagate_function(self.lazy[k], x)
            self.propagate(k, r-l)
            return self.data[k]
        else:
            m = (l+r) // 2
            child_left = self._query(a, b, 2*k+1, l, m)
            child_right = self._query(a, b, 2*k+2, m, r)
            return self.operation_function(child_left, child_right)

    def update(self, a, b, x):
        self._update(a, b, x, 0, 0, self.n_leaf)


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


class TestSegmentTree(unittest.TestCase):
    def test_rmq(self):
        st = SegmentTreeRangeMinimumQuery(5)


if __name__ == "__main__":
    unittest.main()
