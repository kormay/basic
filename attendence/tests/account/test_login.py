from attendence.tests.test_base import TestBase
from django.test import TestCase
from django.core.urlresolvers import resolve, reverse
from django.http import HttpRequest
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import escape

from attendence.views.account import check_old_password
from secu.models import User
from basic.config import ROOTUSER     

from attendence.views.account import login


''' 
    1. 如果是默认用户，则登陆成功并跳转页面
'''    
class Login(TestCase):
    def test_login_by_root_user(self):
        request = HttpRequest()
        request.session = {}
        request.method = 'POST'
        request.META['SERVER_NAME'] = '127.0.0.1'
        request.META['SERVER_PORT'] = '80'

        request.POST['user_name'] = ROOTUSER['name']
        request.POST['pwd'] = ROOTUSER['password']

        response = login(request) 
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('attendence:index', args=None))