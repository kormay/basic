from attendence.tests.test_base import TestBase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import escape

from secu.models import User
from attendence.views import IP

''' 
    1. 如果是GET请求，render Login
    2. 如果是POST请求，删除成功返回1
    3. 如果是POST请求，删除失败，数据不存在返回0
'''


class DeleteIP(TestBase):
    '''
    python manage.py test attendence.tests.test_ip_management.DeleteIP
    '''

    def test_get_request_to_delete_ip(self):
        '''
        python manage.py test attendence.tests.test_ip_management.DeleteIP.test_get_request_to_delete_ip
        '''
        ip = '192.168.1.110'
        self.request.method = 'GET'
        self.request.GET['user_name'] = 'root'
        self.request.GET['ip'] = ip
        self.response = IP.delete(self.request)
        self.assertEqual(self.response.status_code, 200)
        self.assertContains(self.response, 'Login')

    def test_post_request_to_delete_ip(self):
        '''
        python manage.py test attendence.tests.test_ip_management.DeleteIP.test_post_request_to_delete_ip
        '''
        print('test delete...')
        ip = '192.168.1.110'
        self.request.method = 'POST'
        self.request.POST['user_name'] = 'root'
        self.request.POST['ip'] = ip
        IP.add(self.request)
        self.response = IP.delete(self.request)
        print(self.response.content.decode())
        self.assertEqual(self.response.content.decode(), '1')

    def test_post_request_to_delete_ip_not_exists(self):
        '''
        python manage.py test attendence.tests.test_ip_management.DeleteIP.test_post_request_to_delete_ip_not_exists
        '''
        print('test delete...')
        ip = '192.168.1.110'
        self.request.method = 'POST'
        self.request.POST['user_name'] = 'root'
        self.request.POST['ip'] = ip
        self.response = IP.delete(self.request)
        print(self.response.content.decode())
        self.assertEqual(self.response.content.decode(), '0')
