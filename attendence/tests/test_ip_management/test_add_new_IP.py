from attendence.tests.test_base import TestBase
from django.core.urlresolvers import resolve, reverse
from django.http import HttpRequest
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import escape
from secu.models import User

from attendence.views import IP
from django.http.response import JsonResponse
import json
from django.test import TestCase, override_settings
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


'''
1. GET请求初始化页面, 返回status_code=200就成功
2. GET请求添加新的IP，render Login
3. GET请求数据列表，无数据返回
4. GET请求数据列表，有数据返回
5. POST请求添加新的IP，成功返回1
6. POST请求添加新的IP，已存在，添加失败返回0
'''


class AddNewIP(TestBase):
    '''
    python manage.py test attendence.tests.test_ip_management.AddNewIP
    '''
    # @override_settings(DATABASES={
    #     'default': {
    #         'ENGINE': 'django.db.backends.sqlite3',
    #         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #     }
    # })
    @override_settings(RUN_TEST=1)
    def test_get_request_to_load_page(self):
        '''
        python manage.py test attendence.tests.test_ip_management.AddNewIP.test_get_request_to_load_page
        '''
        self.request.method = 'GET'
        self.response = IP.index(self.request)
        self.assertEqual(self.response.status_code, 200)

    def test_get_request_to_add_ip(self):
        '''
        python manage.py test attendence.tests.test_ip_management.AddNewIP.test_get_request_to_add_ip
        '''
        ip = '192.168.1.110'
        self.request.method = 'GET'
        self.request.GET['user_name'] = 'root'
        self.request.GET['ip'] = ip
        self.response = IP.add(self.request)
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, 'Login')

    def test_get_request_for_ip_list_no_data(self):
        '''
        python manage.py test attendence.tests.test_ip_management.AddNewIP.test_get_request_for_ip_list_no_data
        '''

        self.request.method = 'GET'
        self.request.GET['currentpage'] = 1
        self.request.GET['pagesize'] = 10
        self.response = IP.get_list(self.request)
        # print('测试status_code')
        self.assertEqual(self.response.status_code, 200)
        # print('测试response类型')
        self.assertEqual(type(self.response), JsonResponse)
        # print('测试Content-Type')
        items = {k: v for k, v in self.response.items()}
        self.assertEqual(items['Content-Type'], 'application/json')
        # print('测试Content')
        print(self.response.content.decode())
        json_obj = json.loads(self.response.content.decode())
        self.assertEqual(json_obj['totalrecords'], 0)
        self.assertEqual(json_obj['data'], [])

    def test_get_request_for_ip_list_with_data(self):
        '''
        python manage.py test attendence.tests.test_ip_management.AddNewIP.test_get_request_for_ip_list_with_data
        '''

        # 添加数据
        self.request.method = 'POST'
        self.request.POST['user_name'] = 'root'
        self.request.POST['ip'] = '192.168.1.10'
        IP.add(self.request)
        self.request.POST['ip'] = '192.168.1.12'
        IP.add(self.request)

        # 获取数据
        self.request.method = 'GET'
        self.request.GET['currentpage'] = 1
        self.request.GET['pagesize'] = 10
        self.response = IP.get_list(self.request)
        # print('测试status_code')
        self.assertEqual(self.response.status_code, 200)
        # print('测试response类型')
        self.assertEqual(type(self.response), JsonResponse)
        # print('测试Content-Type')
        items = {k: v for k, v in self.response.items()}
        self.assertEqual(items['Content-Type'], 'application/json')
        # print('测试Content')
        # print(self.response.content.decode())
        json_obj = json.loads(self.response.content.decode())
        self.assertEqual(json_obj['totalrecords'], 2)
        for x in json_obj['data']:
            for k, v in x.items():
                print(k, '=>', v)

    def test_post_requtest_add_ip(self):
        '''
        python manage.py test attendence.tests.test_ip_management.AddNewIP.test_post_requtest_add_ip
        '''
        self.request.method = 'POST'
        self.request.POST['user_name'] = 'root'
        self.request.POST['ip'] = '192.168.1.10'
        self.response = IP.add(self.request)
        self.assertEqual(self.response.content.decode(), '1')

    def test_post_requtest_add_ip_already_exists(self):
        '''
        python manage.py test attendence.tests.test_ip_management.AddNewIP.test_post_requtest_add_ip_already_exists
        '''
        self.request.method = 'POST'
        self.request.POST['user_name'] = 'root'
        self.request.POST['ip'] = '192.168.1.10'
        IP.add(self.request)
        # already exists
        self.response = IP.add(self.request)
        self.assertEqual(self.response.content.decode(), '0')
