import unittest
import sys
import os
import json

# BASE_DIR = 'tbd_42'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'common'))


from toutiao import create_app
from settings.testing import TestingConfig


class TestSearchResource(unittest.TestCase):
    """
    测试用户搜索视图接口的单元测试案例
    """
    def setUp(self):
        """
        在测试方法执行之前先被调用
        :return:
        """
        # 使用flask app获取测试客户端的时候，app应该运行在测试模式下
        # app配置   TESTING=True
        app = create_app(TestingConfig)
        self.client = app.test_client()

    def test_normal(self):
        """
        测试正常调用的逻辑
        :return:
        """
        # 构建一个http的请求 发送到用户搜索的接口上
        # 方式1：
        #    采用python中的库发起HTTP请求  urllib  requests
        #    urllib.request.urlopen('http://192.168.10.8:5000/v1_0/search?q=python')
        #    通用，在任何框架中都可以使用这种方式完成web应用的单元测试，
        #    但是，在进行测试的时候，需要将web应用运行起来（flask 程序需要运行起来）之后，才能进行测试
        # 方式2：
        #    采用框架程序提供的测试客户端来模拟发送http请求
        #    flask框架中   提供了一个测试客户端  在flask应用对象中  app=Flask(__name__)
        #    client = app.test_client()  # 注意 test_client是函数，需要调用
        #    client.get('/v1_0/search?q=python')  # 请求路径不需要写运行的ip地址和端口
        #    在测试的时候，不需要web应用程序运行（flask程序无需运行），原因就是测试客户端是框架程序提供的，flask可以直接找到对应的视图执行

        # 接收接口返回的响应数据
        ret = self.client.get('/v1_0/search?q=python')
        # ret -> 响应对象 Response
        # ret.status_code  状态码
        # ret.data  响应体 json str

        # 判断响应数据是否符合预期
        # 判断状态码
        # assert ret.status_code == 200
        self.assertEqual(ret.status_code, 200)

        # 判断响应体
        resp_data = ret.data
        resp_dict = json.loads(resp_data)

        self.assertIn('message', resp_dict)
        self.assertEqual(resp_dict['message'], 'OK')
        self.assertIn('data', resp_dict)
        data = resp_dict['data']
        self.assertIn('total_count', data)
        self.assertIn('page', data)
        self.assertIn('per_page', data)
        self.assertIn('results', data)

    def test_missing_q_param_error(self):
        """
        测试q请求参数未传递的情况
        :return:
        """
        ret = self.client.get('/v1_0/search')

        self.assertEqual(ret.status_code, 400)

        resp_data = ret.data
        resp_dict = json.loads(resp_data)

        self.assertIn('message', resp_dict)
        self.assertIn('q', resp_dict['message'])

    def test_q_param_length_error(self):
        """
        测试q请求参数长度异常的情况
        :return:
        """
        q = 'e' * 51

        ret = self.client.get('/v1_0/search?q={}'.format(q))

        self.assertEqual(ret.status_code, 400)

        resp_data = ret.data
        resp_dict = json.loads(resp_data)

        self.assertIn('message', resp_dict)
        self.assertIn('q', resp_dict['message'])


if __name__ == '__main__':
    unittest.main()









