
import unittest
import sys

sys.setrecursionlimit(100_000 * 3)


class Point:
    def __init__(self, position, value):
        self.position = position
        self.value = value


class Node:
    def __init__(self, position, value, left_child, right_child):
        self.position = position
        self.value = value
        self.left_child = left_child
        self.right_child = right_child


class KdTree:
    def __init__(self, points):
        if not points:
            return None
        self.dimension = len(points[0].position)
        self.root = self.build(points)

    def build(self, points, depth=0):
        if not points:
            return None
        axis = depth % self.dimension
        pivot, left_points, right_points = self.partition(points, axis)

        return Node(
            pivot.position,
            pivot.value,
            self.build(left_points, depth + 1),
            self.build(right_points, depth + 1),
        )

    def partition(self, points, axis):
        if len(points) < 3:
            points.sort(key=lambda p: p.position[axis])
            return points[0], [], points[1:]

        sorted_three_element = sorted(
            points[:3], key=lambda p: p.position[axis])
        pivot = sorted_three_element[1]
        left = [sorted_three_element[0]]
        right = [sorted_three_element[2]]

        for v in points[3:]:
            if v.position[axis] <= pivot.position[axis]:
                left.append(v)
            else:
                right.append(v)
        return pivot, left, right

    def list(self, lb, ub):
        return self._list(self.root, 0, lb, ub)

    def _list(self, node, depth, lb, ub):
        ret = []
        p = node.position
        if all(lb[i] <= p[i] < ub[i] for i in range(self.dimension)):
            ret.append(node.value)
        axis = depth % self.dimension
        if node.left_child and lb[axis] <= p[axis]:
            ret.extend(self._list(node.left_child, depth + 1, lb, ub))
        if node.right_child and p[axis] < ub[axis]:
            ret.extend(self._list(node.right_child, depth + 1, lb, ub))
        return ret

    def count(self, lb, ub):
        return self._count(self.root, 0, lb, ub)

    def _count(self, node, depth, lb, ub):
        cnt = 0
        p = node.position
        if all(lb[i] <= p[i] < ub[i] for i in range(self.dimension)):
            cnt += 1
        axis = depth % self.dimension
        if node.left_child and lb[axis] <= p[axis]:
            cnt += self._count(node.left_child, depth + 1, lb, ub)
        if node.right_child and p[axis] < ub[axis]:
            cnt += self._count(node.right_child, depth + 1, lb, ub)
        return cnt


class TestKdTree(unittest.TestCase):
    def test_1d_tree_count(self):
        kdtree = KdTree([
            Point((1,), 0),
            Point((2,), 1),
            Point((6,), 2),
            Point((3,), 3),
            Point((5,), 4),
        ])
        self.assertEqual(kdtree.count((2,), (4,)), 2)
        self.assertEqual(kdtree.count((0,), (1,)), 0)
        self.assertEqual(kdtree.count((5,), (6,)), 1)
        self.assertEqual(kdtree.count((1,), (100,)), 5)
        self.assertEqual(kdtree.count((10,), (100,)), 0)

    def test_2d_tree_count(self):
        kdtree = KdTree([
            Point((1, 1), 0),
            Point((2, 3), 1),
            Point((6, 2), 2),
            Point((3, 8), 3),
            Point((5, 1), 4),
        ])
        self.assertEqual(kdtree.count((2, 4), (4, 9)), 1)
        self.assertEqual(kdtree.count((0, 0), (1, 1)), 0)
        self.assertEqual(kdtree.count((5, 1), (6, 2)), 1)
        self.assertEqual(kdtree.count((1, 1), (100, 100)), 5)
        self.assertEqual(kdtree.count((10, 0), (100, 100)), 0)

    def test_3d_tree_count(self):
        kdtree = KdTree([
            Point((1, 1, 1), 0),
            Point((2, 3, 4), 1),
            Point((6, 2, 4), 2),
            Point((3, 8, 7), 3),
            Point((5, 1, 2), 4),
        ])
        self.assertEqual(kdtree.count((2, 4, 0), (4, 9, 10)), 1)
        self.assertEqual(kdtree.count((0, 0, 0), (1, 1, 1)), 0)
        self.assertEqual(kdtree.count((5, 1, 1), (6, 2, 3)), 1)
        self.assertEqual(kdtree.count((1, 1, 1), (10, 10, 10)), 5)
        self.assertEqual(kdtree.count((10, 0, 0), (100, 100, 100)), 0)

    def test_1d_tree_list(self):
        kdtree = KdTree([
            Point((1,), 0),
            Point((2,), 1),
            Point((6,), 2),
            Point((3,), 3),
            Point((5,), 4),
        ])
        self.assertEqual(sorted(kdtree.list((2,), (4,))), [1, 3])
        self.assertEqual(sorted(kdtree.list((0,), (1,))), [])
        self.assertEqual(sorted(kdtree.list((5,), (6,))), [4])
        self.assertEqual(sorted(kdtree.list((1,), (100,))), [0, 1, 2, 3, 4])
        self.assertEqual(sorted(kdtree.list((10,), (100,))), [])

    def test_2d_tree_list(self):
        kdtree = KdTree([
            Point((1, 1), 0),
            Point((2, 3), 1),
            Point((6, 2), 2),
            Point((3, 8), 3),
            Point((5, 1), 4),
        ])
        self.assertEqual(sorted(kdtree.list((2, 4), (4, 9))), [3])
        self.assertEqual(sorted(kdtree.list((0, 0), (1, 1))), [])
        self.assertEqual(sorted(kdtree.list((5, 1), (6, 2))), [4])
        self.assertEqual(
            sorted(kdtree.list((1, 1), (100, 100))), [0, 1, 2, 3, 4])
        self.assertEqual(sorted(kdtree.list((10, 0), (100, 100))), [])


if __name__ == '__main__':
    unittest.main()
