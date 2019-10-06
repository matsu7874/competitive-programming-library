import unittest
import random


import data_structure.segmenttree as segmenttree


def bruteforce(points, lb, ub):
    cnt = 0
    dimension = len(lb)
    for p in points:
        if all(lb[i] <= p[i] < ub[i] for i in range(dimension)):
            cnt += 1
    return cnt


class TestSegmentTree(unittest.TestCase):
    def test_rmq(self):
        pass
        # st = segmenttree.SegmentTree(list(p[0:1] for p in self.points))
        # for query in self.queries:
        #     lb = [q[0] for q in query[0:1]]
        #     ub = [q[1] for q in query[0:1]]
        #     cnt_kd = kd.count(lb, ub)
        #     cnt_b = bruteforce(self.points, lb, ub)
        #     self.assertEqual(cnt_kd, cnt_b)


if __name__ == '__main__':
    unittest.main()
