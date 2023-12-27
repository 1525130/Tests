import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_search(self):
        """ 浏览器自动化测试示例代码 """

        # 待搜索的关键字
        keyword1 = 'python'

        # 访问网站
        self.driver.get('https://www.baidu.com/')
        self.driver.implicitly_wait(2)

        # 输入关键字
        self.driver.find_element(By.ID, 'kw').send_keys(keyword1)
        self.driver.implicitly_wait(2)

        # 点击按钮
        self.driver.find_element(By.ID, 'su').click()
        self.driver.implicitly_wait(2)

        # 获取网页上的关键字
        keyword2 = self.driver.find_element(By.ID, 'kw').get_property('value')

        self.assertEqual(keyword1, keyword2)


if __name__ == '__main__':
    unittest.main()
