from attendence.tests.test_base import TestBase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import escape

from attendence.views.account import check_old_password
from secu.models import User

''' 
    1. 如果是GET请求，return None
    2. 如果是POST请求，old password正确，返回信息：''
    3. 如果是POST请求，old password不正确，返回信息： 'Your old password incorrect, please try again.'
'''    
class CheckOldPassword(TestBase):
    def test_get_request_return_none(self):
        self.request.method = 'GET'
        self.assertEqual(check_old_password(self.request), None)

    def test_post_request_by_correct_password(self):
        self.request.method = 'POST'
        self.request.POST['old_password'] = 'max123'
        self.response = check_old_password(self.request)
        self.assertEqual(self.response.content.decode(), '')

    def test_post_request_by_incorrect_password(self):
        self.request.method = 'POST'
        self.request.POST['old_password'] = 'incorrect_password'
        self.response = check_old_password(self.request) 
        self.assertEqual(self.response.content.decode(), 'Your old password incorrect, please try again.')
        # 如果不加上.decode()：结果为 b'message', 对应方法 encode()
