"""
Shift-And
オンライン文字列検索アルゴリズム

"""
import unittest


def search(pattern, text):
    # preprocessing
    n = len(text)
    m = len(pattern)
    mask = {c: 0 for i, c in enumerate(pattern)}
    for i,c in enumerate(pattern):
        mask[c] |= 1 << (i)

    # searching
    res = []
    state = 0
    for pos in range(n):
        state = ((state << 1) | 1) & mask[text[pos]] if text[pos] in mask else 0
        if state & 1 << (m - 1):
            res.append(pos - m + 1)
    return res


class TestShiftAnd(unittest.TestCase):
    def test_shift_and(self):
        pattern = 'ac'
        text = 'abcacbbca'
        self.assertEqual(search(pattern, text), [3])

        pattern = 'announce'
        text = 'CPM_annual_conference_announce'
        self.assertEqual(search(pattern, text), [22])

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
