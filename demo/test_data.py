import unittest

from utils.data import data_driven, data_inject


@data_driven
class MyTestCase(unittest.TestCase):
    @data_inject([
        0,
        1,
    ])
    def test_equal(self, n):
        self.assertEqual(0, n)

    @data_inject([
        (1, 2, 3),
        (4, 5, 6),
    ])
    def test_plus(self, a, b, c):
        """ 测试前两个数的和是否等于第三个数 """
        self.assertEqual(a + b, c)

    @data_inject([
        {'m': 1, 'n': 1, 's': 1},
        {'m': 2, 'n': 2, 's': 2},
    ])
    def test_multiply(self, m, n, s):
        self.assertEqual(m * n, s)


if __name__ == '__main__':
    unittest.main()
