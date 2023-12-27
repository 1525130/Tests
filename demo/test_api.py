import unittest
import requests


class MyTestCase(unittest.TestCase):
    def test_get(self):
        """ 接口测试示例代码(GET请求) """

        url = 'https://www.httpbin.org/get'
        response = requests.get(url)

        self.assertEqual(response.json().get('url'), url)

    @unittest.skip('Do not test this case')
    def test_post(self):
        """ 接口测试示例代码(POST请求) """

        url = 'https://www.httpbin.org/post'
        response = requests.post(url)

        self.assertNotEqual(response.json().get('url'), url)


if __name__ == '__main__':
    unittest.main()
