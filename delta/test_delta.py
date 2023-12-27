import requests
import unittest

from utils.data import data_driven, data_inject

BASE_URL = 'your_base_url'
USERNAME = 'your_username'
PASSWORD = 'your_password'


@data_driven
class MyTestCase(unittest.TestCase):
    def setUp(self):
        response = requests.post(f'{BASE_URL}/users/login/', json={'username': USERNAME, 'password': PASSWORD})
        self.token = response.json()

    def test_case1(self):
        """ 策略管理-板块管理-查看成分 """

        response = requests.get(
            url=f'{BASE_URL}/api/v1/node/data',
            params={
                'asset_type': 'Stk',
                'module': 'Category',
                'data_id': 'CN|申万行业分类(新)|房地产|房地产开发|产业地产|system',
            },
            headers={
                'Authorization': self.token,
                'X-Service-Name': 'data_center',
            }
        )

        self.assertEqual(response.json()['msg'], 'ok')

    @data_inject([
        'GLOBAL|StkInx|SW01-房地产|申万行业2021-房地产',
        'GLOBAL|StkInx|SW01-美容护理|申万行业2021-美容护理',
    ])
    def test_case2(self, uid):
        """ 策略管理-策略构建-公共指数 """

        response = requests.get(
            url=f'{BASE_URL}/api/v1/index',
            params={
                'uid': uid,
            },
            headers={
                'Authorization': self.token,
                'X-Service-Name': 'data_center',
            }
        )

        self.assertEqual(response.json()['msg'], 'ok')


if __name__ == '__main__':
    unittest.main()
