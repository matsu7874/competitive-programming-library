import unittest


class PrimeFactorization:
    def __init__(self, upper_limit):
        _primes, minimam_prime_factor = PrimeFactorization.list_primes(
            upper_limit)
        self.minimam_prime_factor = minimam_prime_factor

    def list_primes(upper_limit):
        # Sieve of Eratosthenes
        if upper_limit <= 2:
            return [], [0, 1]

        minimam_prime_factor = [i if i %
                                2 == 1 else 2 for i in range(upper_limit)]
        minimam_prime_factor[0] = 0
        primes = [2]
        is_prime = [i % 2 == 1 for i in range(upper_limit)]
        for i in range(3, upper_limit, 2):
            if not is_prime[i]:
                continue
            primes.append(i)
            for j in range(i*i, upper_limit, i):
                is_prime[j] = False
                if minimam_prime_factor[j] == j:
                    minimam_prime_factor[j] = i
        return primes, minimam_prime_factor

    def list_prime_factors(self, n) -> set:
        factors = set()
        while 1 < n:
            factors.add(self.minimam_prime_factor[n])
            n //= self.minimam_prime_factor[n]
        return factors


class TestPrimeFactorization(unittest.TestCase):
    def test1(self):
        primes, minimam_prime_factor = PrimeFactorization.list_primes(1)
        self.assertEqual(primes, [])
        self.assertEqual(minimam_prime_factor, [0, 1])

    def test2(self):
        primes, minimam_prime_factor = PrimeFactorization.list_primes(2)
        self.assertEqual(primes, [])
        self.assertEqual(minimam_prime_factor, [0, 1])

    def test3(self):
        primes, minimam_prime_factor = PrimeFactorization.list_primes(3)
        self.assertEqual(primes, [2])
        self.assertEqual(minimam_prime_factor, [
                         0, 1, 2])

    def test20(self):
        primes, minimam_prime_factor = PrimeFactorization.list_primes(20)
        self.assertEqual(primes, [2, 3, 5, 7, 11, 13, 17, 19])
        self.assertEqual(minimam_prime_factor, [
                         0, 1, 2, 3, 2, 5, 2, 7, 2, 3, 2, 11, 2, 13, 2, 3, 2, 17, 2, 19])


def is_prime(n: int) -> bool:
    """
    素数判定
    O(n^0.5)
    """
    if n == 2 or n == 3:
        return True
    if n < 2 or n & 1 == 0 or n % 3 == 0:
        return False
    for i in range(5, int(n**0.5) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True


def genarate_primes(n: int) -> list:
    """
    素数リスト(Sieve of Eratosthenes)
    N以下の素数のリストを返す
    O(n loglogn)
    """
    if n == 2:
        return [2]
    if n == 3:
        return [2, 3]
    if n < 2:
        return []

    is_prime = [True] * (n + 1)
    for i in range(3, n + 1, 3):
        is_prime[i] = False

    for i in range(5, int(n**0.5 + 1), 6):
        if is_prime[i]:
            for j in range(i * i, n + 1, i):
                is_prime[j] = False
        if is_prime[i + 2]:
            for j in range((i + 2) * (i + 2), n + 1, (i + 2)):
                is_prime[j] = False

    return [2, 3] + [i for i in range(5, n + 1, 2) if is_prime[i]]


def prime_factorize(n: int) -> list:
    """
    素因数分解
    """
    if n < 2:
        return []
    prime_factors = []
    while n % 2 == 0:
        prime_factors.append(2)
        n >>= 1

    while n % 3 == 0:
        prime_factors.append(3)
        n //= 3

    a = 5
    b = 7
    while a ** 2 <= n:
        if n % a == 0:
            prime_factors.append(a)
            n //= a
        elif n % b == 0:
            prime_factors.append(b)
            n //= b
        else:
            a += 6
            b += 6
    if n > 1:
        prime_factors.append(n)
    return prime_factors


def prime_factorize_by_primes(n, sorted_primes=[]):
    # 素因数分解
    prime_factors = []
    if n < 2:
        return prime_factors
    i = 0
    while sorted_primes[i]**2 <= n:
        if n % sorted_primes[i] == 0:
            prime_factors.append(sorted_primes[i])
            n //= sorted_primes[i]
        else:
            i += 1
    if n > 1:
        prime_factors.append(n)
    return prime_factors


class TestIsPrime(unittest.TestCase):
    def test_prime(self):
        self.assertTrue(is_prime(2))
        self.assertTrue(is_prime(3))
        self.assertTrue(is_prime(5))
        self.assertTrue(is_prime(7))
        self.assertTrue(is_prime(11))
        self.assertTrue(is_prime(13))

    def test_big_prime(self):
        self.assertTrue(is_prime(8191))
        self.assertTrue(is_prime(67280421310721))

    def test_composite(self):
        self.assertFalse(is_prime(1))
        self.assertFalse(is_prime(4))
        self.assertFalse(is_prime(6))
        self.assertFalse(is_prime(8))
        self.assertFalse(is_prime(9))


class TestGenaratePrimes(unittest.TestCase):
    def test_generate_primes(self):
        self.assertEqual(genarate_primes(
            35), [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31])


class TestPrimeFactorize(unittest.TestCase):
    def test_prime_factorize(self):
        self.assertEqual(prime_factorize(2), [2])
        self.assertEqual(prime_factorize(3), [3])
        self.assertEqual(prime_factorize(8), [2, 2, 2])
        self.assertEqual(prime_factorize(18), [2, 3, 3])
        self.assertEqual(prime_factorize(35), [5, 7])


if __name__ == '__main__':
    unittest.main()
