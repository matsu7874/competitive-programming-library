import random
import unittest


def miller_rabin(n: int, k=100) -> bool:
    """
    素数判定
    2^64以下については決定的アルゴリズム
    2^64を超える数について、間違う確率は4^-k

    """
    if n == 2:
        return True
    if n < 2 or n & 1 == 0:
        return False

    if n < 2**64:
        witnesses = [x for x in [2, 3, 5, 7, 11,
                                 13, 17, 19, 23, 29, 31, 37] if x < n]
    else:
        witnesses = [random.randint(1, n - 1) for _ in range(k)]

    d = (n - 1) >> 1
    while d & 1 == 0:
        d >>= 1
    for a in witnesses:
        t = d
        y = pow(a, t, n)
        while t != n - 1 and y != 1 and y != n - 1:
            y = pow(y, 2, n)
            t <<= 1
        if y != n - 1 and t & 1 == 0:
            return False
    return True


class TestMillerRabin(unittest.TestCase):
    def test_prime(self):
        self.assertTrue(miller_rabin(2))
        self.assertTrue(miller_rabin(3))
        self.assertTrue(miller_rabin(5))
        self.assertTrue(miller_rabin(7))
        self.assertTrue(miller_rabin(11))
        self.assertTrue(miller_rabin(13))

    def test_big_prime(self):
        self.assertTrue(miller_rabin(8191))
        self.assertTrue(miller_rabin(67280421310721))
        self.assertTrue(miller_rabin(170141183460469231731687303715884105727))
        self.assertTrue(miller_rabin(
            20988936657440586486151264256610222593863921))

    def test_composite(self):
        self.assertFalse(miller_rabin(1))
        self.assertFalse(miller_rabin(4))
        self.assertFalse(miller_rabin(6))
        self.assertFalse(miller_rabin(8))
        self.assertFalse(miller_rabin(9))


if __name__ == '__main__':
    unittest.main()
