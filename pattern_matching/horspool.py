"""
horspoolのオンライン文字列検索アルゴリズム

suffix searchでsearch windowの最後の文字に応じたスキップを行う。
"""
import unittest


def horspool(pattern, text):
    # preprocessing
    n = len(text)
    m = len(pattern)
    d = {c: m for c in pattern[:-1]}
    for i in range(m - 1):
        d[pattern[i]] = m - 1 - i

    # searching
    pos = 0
    res = []
    while pos <= n - m:
        i = m - 1
        while i >= 0 and text[pos + i] == pattern[i]:
            i -= 1
        if i == -1:
            res.append(pos)
        pos += d[text[pos + m - 1]] if text[pos + m - 1] in d else m
    return res


class TestHorspool(unittest.TestCase):
    def test_horspool(self):
        pattern = 'ac'
        text = 'abcacbbca'
        self.assertEqual(horspool(pattern, text), [3])

        pattern = 'announce'
        text = 'CPM_annual_conference_announce'
        self.assertEqual(horspool(pattern, text), [22])

        pattern = 'a'
        text = 'a'
        self.assertEqual(horspool(pattern, text), [0])

        pattern = 'z'
        text = 'abcde'
        self.assertEqual(horspool(pattern, text), [])

        pattern = 'a'
        text = 'abababa'
        self.assertEqual(horspool(pattern, text), [0, 2, 4, 6])

        pattern = 'aaa'
        text = 'aaaaaa'
        self.assertEqual(horspool(pattern, text), [0, 1, 2, 3])

        pattern = 'aba'
        text = 'abababa'
        self.assertEqual(horspool(pattern, text), [0, 2, 4])


if __name__ == '__main__':
    unittest.main()
