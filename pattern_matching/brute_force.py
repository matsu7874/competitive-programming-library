"""
力任せなオンライン文字列検索アルゴリズム
"""

import unittest

def search(pattern, text):
    n = len(text)
    m = len(pattern)
    res = []
    for i in range(n - m + 1):
        if text[i:i + m] == pattern:
            res.append(i)
    return res


class TestBruteForce(unittest.TestCase):
    def test_search(self):
        pattern = 'a'
        text = 'a'
        self.assertEqual(search(pattern, text), [0])

        pattern = 'z'
        text = 'abcde'
        self.assertEqual(search(pattern, text), [])

        pattern = 'a'
        text = 'abababa'
        self.assertEqual(search(pattern, text), [0, 2, 4, 6])

        pattern = 'aaa'
        text = 'aaaaaa'
        self.assertEqual(search(pattern, text), [0, 1, 2, 3])

        pattern = 'aba'
        text = 'abababa'
        self.assertEqual(search(pattern, text), [0, 2, 4])

if __name__ == '__main__':
    unittest.main()
