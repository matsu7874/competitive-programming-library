import unittest
import random

from data_structure.kdtree import KdTree, Point

def bruteforce(points, lb, ub):
    cnt = 0
    dimension = len(lb)
    for p in points:
        if all(lb[i] <= p[i] < ub[i] for i in range(dimension)):
            cnt += 1
    return cnt

class TestKdTree(unittest.TestCase):
    points = list(list(random.randint(1, 1000000) for j in range(3)) for i in range(1000))
    queries = list(list((random.randint(1, 500000), random.randint(500001, 1000000)) for j in range(3)) for i in range(1000))
    
    def test_1d_tree(self):
        kd = KdTree([Point(p[0:1], i) for i,p in enumerate(self.points)])
        for query in self.queries:
            lb = [q[0] for q in query[0:1]]
            ub = [q[1] for q in query[0:1]]
            cnt_kd = kd.count(lb, ub)
            cnt_b = bruteforce(self.points, lb, ub)
            self.assertEqual(cnt_kd, cnt_b)
    def test_2d_tree(self):
        kd = KdTree([Point(p[0:2], i) for i,p in enumerate(self.points)])
        for query in self.queries:
            lb = [q[0] for q in query[0:2]]
            ub = [q[1] for q in query[0:2]]
            cnt_kd = kd.count(lb, ub)
            cnt_b = bruteforce(self.points, lb, ub)
            self.assertEqual(cnt_kd, cnt_b)

    def test_3d_tree(self):
        kd = KdTree([Point(p[0:3], i) for i,p in enumerate(self.points)])
        for query in self.queries:
            lb = [q[0] for q in query[0:3]]
            ub = [q[1] for q in query[0:3]]
            cnt_kd = kd.count(lb, ub)
            cnt_b = bruteforce(self.points, lb, ub)
            self.assertEqual(cnt_kd, cnt_b)

    
if __name__ == '__main__':
    unittest.main()
