# 木の定義
class Tree:
    def __init__(self, pickle_file=None):
        self.root = None

    def build_fc_tree(self, elms):
        """Elmsから木を作成する"""
        assert len(elms) > 0, 'no elm in input data'
        assert len(elms) == len(
            set(elms)), 'The same data exists for name and location.'
        if len(elms) > 0:
            sbx = [ArrayElm(elm) for elm in sorted(
                elms, key=lambda elm: elm.loc)]  # sorted by x
            sby = [ArrayElm(elm) for elm in sorted(
                elms, key=lambda elm: elm.loc_rev())]  # sorted by y
            self.root = self._build_fc_tree(sbx, sby)

    def _linked_array(self, array, array_l, array_r):
        """arrayからarray_l, array_rにminmax, maxminリンクを張る"""
        for array_elm in array:
            array_elm.bleft = self._find_minmax_ix(array_l, array_elm.elm)
            array_elm.bright = self._find_minmax_ix(array_r, array_elm.elm)
            array_elm.eleft = self._find_maxmin_ix(array_l, array_elm.elm)
            array_elm.eright = self._find_maxmin_ix(array_r, array_elm.elm)
        return array

    def _build_fc_tree(self, sbx, sby):
        """層状領域木の作成"""
        if len(sbx) == 1:
            v = Node(sbx[0].loc())
            v.array = sby
        else:
            n = len(sbx)
            pivot = sbx[n//2-1].loc()
            sbx_l = sbx[:n//2]
            sbx_r = sbx[n//2:]
            sby_l = [ArrayElm(array_elm.elm)
                     for array_elm in sby if array_elm.loc() <= pivot]
            sby_r = [ArrayElm(array_elm.elm)
                     for array_elm in sby if array_elm.loc() > pivot]
            v = Node(pivot)
            v.array = self._linked_array(sby, sby_l, sby_r)
            v.left = self._build_fc_tree(sbx_l, sby_l)
            v.right = self._build_fc_tree(sbx_r, sby_r)
        return v

    def fc_range_query(self, R):
        """generator: 領域Rに含まれるノードを返す"""
        com_R = Rectangle(x_min=(R.x_min, -float('inf')), x_max=(R.x_max, float('inf')),
                          y_min=(R.y_min, -float('inf')), y_max=(R.y_max, float('inf')))
        for elm in self._fc_range_query(self, com_R):
            yield elm

    def _fc_range_query(self, tree, com_R):
        """長方形領域R内に存在するデータを出力する(class Elm)"""
        begin_x, end_x = com_R.x_min, com_R.x_max
        begin_y, end_y = com_R.y_min, com_R.y_max
        v_split = self._find_split_node(tree, begin_x, end_x)
        virtual_begin_elm = Elm(name='vbe', loc=(
            begin_y[1], begin_y[0]))  # minmax_ixを求める用
        virtual_end_elm = Elm(name='vee', loc=(
            end_y[1], end_y[0]))     # maxmin_ixを求める用
        minmax_ix = self._find_minmax_ix(v_split.array, virtual_begin_elm)
        maxmin_ix = self._find_maxmin_ix(v_split.array, virtual_end_elm)
        if minmax_ix is None or maxmin_ix is None:
            return None
        minmax_key = v_split.array[minmax_ix]
        maxmin_key = v_split.array[maxmin_ix]

        if v_split.is_leaf():
            if v_split.array[0].is_included(com_R):
                yield v_split.array[0]
        else:
            v = v_split.left
            lb_p = minmax_key.bleft  # left begin pointer
            le_p = maxmin_key.eleft  # left end pointer
            while not lb_p is None\
                    and not le_p is None\
                    and not v.is_leaf():
                if v.loc >= begin_x:
                    begin_p = v.array[lb_p].bright
                    end_p = v.array[le_p].eright
                    for elm in self._frac_casc(v.right.array, begin_p, end_p):
                        yield elm
                    lb_p = v.array[lb_p].bleft
                    le_p = v.array[le_p].eleft
                    v = v.left
                else:
                    lb_p = v.array[lb_p].bright
                    le_p = v.array[le_p].eright
                    v = v.right
            if not lb_p is None\
                    and not le_p is None\
                    and v.array[0].is_included(com_R):
                yield v.array[0]

            v = v_split.right
            rb_p = minmax_key.bright  # right begin pointer
            re_p = maxmin_key.eright  # right end pointer
            while not rb_p is None\
                    and not re_p is None\
                    and not v.is_leaf():
                if v.loc <= end_x:
                    begin_p = v.array[rb_p].bleft
                    end_p = v.array[re_p].eleft
                    for x in self._frac_casc(v.left.array, begin_p, end_p):
                        yield x
                    rb_p = v.array[rb_p].bright
                    re_p = v.array[re_p].eright
                    v = v.right
                else:
                    rb_p = v.array[rb_p].bleft
                    re_p = v.array[re_p].eleft
                    v = v.left
            if not rb_p is None\
                    and not re_p is None\
                    and v.array[0].is_included(com_R):
                yield v.array[0]

    def _find_maxmin_ix(self, array, elm):
        """(y座標, x座標)に対して array中のmaxminインデックスを返す"""
        lo, hi = 0, len(array)
        if elm.loc_rev() < array[lo].loc_rev():
            return None
        while lo < hi:
            mid = (lo+hi)//2
            if elm.loc_rev() < array[mid].loc_rev():
                hi = mid
            else:
                lo = mid+1
        return lo-1

    def _frac_casc(self, array, begin_pointer, end_pointer):
        if begin_pointer is not None and end_pointer is not None:
            for ix in range(begin_pointer, end_pointer+1):
                yield array[ix]

    def _find_split_node(self, tree, begin, end):
        """beginへの探索経路とendへの探索経路が分岐する節点v, または両方の経路がともに終了する葉節点v"""
        v = tree.root
        while not v.is_leaf() and not begin <= v.loc < end:
            if v.loc >= end:
                v = v.left
            else:
                v = v.right
        return v

    def _find_minmax_ix(self, array, elm, reverse=False):
        """(y座標, x座標)に対して array中のminmaxインデックスを返す"""
        lo, hi = 0, len(array)
        if elm.loc_rev() > array[hi-1].loc_rev():
            return None
        while lo < hi:
            mid = (lo+hi)//2
            if array[mid].loc_rev() < elm.loc_rev():
                lo = mid+1
            else:
                hi = mid
        return lo
# 節の定義


class Node:
    def __init__(self, loc):
        self.loc = loc  # location
        self.left = None
        self.right = None
        self.array = None

    def is_leaf(self):
        if self.left is None and self.right is None:
            return True
        else:
            return False

    def __str__(self):
        return str(self.loc)

# 要素の定義


class Elm:
    def __init__(self, name, loc):
        self.name = name
        self.loc = *loc, name

    def loc_rev(self):
        return self.loc[1], self.loc[0]

    def is_included(self, com_R):
        lon, lat, _ = self.loc
        if com_R.x_min <= (lon, lat) <= com_R.x_max\
                and com_R.y_min <= (lat, lon) <= com_R.y_max:
            return True
        else:
            return False

    def __eq__(self, other):
        return (self.name, self.loc) == (other.name, other.loc)

    def __hash__(self):
        return hash((self.name, self.loc))

    def __str__(self):
        return f'name: {self.name}, loc: ({self.loc[0]}, {self.loc[1]})'

# 配列の要素の定義


class ArrayElm:
    def __init__(self, elm):
        self.elm = elm
        self.bleft = None  # left_begin_pointer
        self.bright = None  # right_begin_pointer
        self.eleft = None  # left_end_pointer
        self.eright = None  # left_end_pointer

    def loc(self):
        return self.elm.loc

    def loc_rev(self):
        return self.elm.loc_rev()

    def is_included(self, R):
        return self.elm.is_included(R)

    def __str__(self):
        return self.elm.__str__()

# 長方形領域


class Rectangle:
    def __init__(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def __str__(self):
        return f'Rectangle: [{self.x_min}, {self.x_max}] * [{self.y_min}, {self.y_max}]'


if __name__ == '__main__':

    # 実行のサンプル

    # データ準備
    sample_data = list()
    sample_data.append(Elm(name='A', loc=(1, 5)))  # loc(x座標, y座標)
    sample_data.append(Elm(name='B', loc=(2, 2)))
    sample_data.append(Elm(name='C', loc=(4, 8)))
    sample_data.append(Elm(name='D', loc=(5, 7)))
    sample_data.append(Elm(name='E', loc=(5, 5)))
    sample_data.append(Elm(name='F', loc=(8, 6)))
    sample_data.append(Elm(name='E', loc=(7, 1)))

    # 木のインスタンスの作成
    tree = Tree()
    # sample_dataを用いて層状領域木を作成
    tree.build_fc_tree(sample_data)

    # 探索領域を指定
    R = Rectangle(x_min=1.5, x_max=5.5,
                  y_min=1.5, y_max=5.5)

    # フラクショナルカスケーディングを実行 / 結果の出力
    for elm in tree.fc_range_query(R):
        print(elm)
