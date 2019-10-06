
import unittest
import sys

sys.setrecursionlimit(100_000 * 3)


class RangeTree2D:
    class Node:
        def __init__(self, value, left_child, right_child):
            self.value = value
            self.left_child = left_child
            self.right_child = right_child

    def __init__(self, points):
        if not points:
            return None
        self.dimension = len(points[0])
        self.root = self.build(points)

    def build(self, points, depth=0):
        if not points:
            return None
        axis = depth % self.dimension
        pivot, left_points, right_points = self.partition(points, axis)

        return self.Node(
            pivot,
            self.build(left_points, depth + 1),
            self.build(right_points, depth + 1),
        )

    def partition(self, points, axis):
        if len(points) < 3:
            points.sort(key=lambda x: x[axis])
            return points[0], [], points[1:]

        sorted_three_element = sorted(points[:3], key=lambda x: x[axis])
        pivot = sorted_three_element[1]
        left = [sorted_three_element[0]]
        right = [sorted_three_element[2]]

        for v in points[3:]:
            if v[axis] <= pivot[axis]:
                left.append(v)
            else:
                right.append(v)
        return pivot, left, right

    def count(self, lb, ub):
        return self._count(self.root, 0, lb, ub)

    def _count(self, node, depth, lb, ub):
        cnt = 0
        p = node.value
        if all(lb[i] <= p[i] < ub[i] for i in range(self.dimension)):
            cnt += 1
        axis = depth % self.dimension
        if node.left_child and lb[axis] <= p[axis]:
            cnt += self._count(node.left_child, depth + 1, lb, ub)
        if node.right_child and p[axis] < ub[axis]:
            cnt += self._count(node.right_child, depth + 1, lb, ub)
        return cnt


class TestKdTree(unittest.TestCase):
    def test_2d_tree(self):
        rt = RangeTree2D([(1, 1), (2, 3), (6, 2), (3, 8), (5, 1), ])
        self.assertEqual(rt.count((2, 4), (4, 9)), 1)
        self.assertEqual(rt.count((0, 0), (1, 1)), 0)
        self.assertEqual(rt.count((5, 1), (6, 2)), 1)
        self.assertEqual(rt.count((1, 1), (100, 100)), 5)
        self.assertEqual(rt.count((10, 0), (100, 100)), 0)


if __name__ == '__main__':
    unittest.main()
