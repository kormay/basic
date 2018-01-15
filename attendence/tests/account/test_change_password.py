from attendence.tests.test_base import TestBase
from django.core.urlresolvers import resolve, reverse
from django.http import HttpRequest
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import escape

from attendence.views.account import change_password
from secu.models import User

''' 
    1. 如果是GET请求，初始化页面
    2. 如果是POST请求，old password为空，不修改密码，提示信息: Please enter your old password.
    3. 如果是POST请求，old password不正确，提示信息: Please enter your old password.
    3. 如果是POST请求，new password为空，不修改密码，提示信息: Please enter your new password.
    4. 如果是POST请求，confirm password为空，不修改密码，提示信息: Please enter your confirm password.
    5. 如果是POST请求，confirm password 不等于 new password，提示信息: The confirm password not match with the new password, please try again.
    6. 如果是POST请求，old password 等于 new password，提示信息: The new password was the same as your old password, please try again.
    7. 如果是POST请求，old password错误，提示信息: Your old password incorrect, please try again.
    8. 如果是POST请求，用户密码修改成new password，跳转至登录页面

'''    
class ChangePassword(TestBase):
    def test_get_request_render_to_change_password_page(self):
        self.request.method = 'GET'
        self.response = change_password(self.request)
        self.assertContains(self.response, '修改密码') # assertNotContains
        self.assertEqual(self.response.status_code, 200)

    def test_post_request_old_password_is_empty(self):
        self.request.method = 'POST'
        self.request.POST['old_password'] = ''
        self.response = change_password(self.request)
        self.assertContains(self.response, 'Please enter your old password.')

    def test_post_request_new_password_is_empty(self):
        self.request.method = 'POST'
        self.request.POST['old_password'] = 'admin'
        self.request.POST['new_password'] = ''
        self.response = change_password(self.request)
        self.assertContains(self.response, 'Please enter your new password.')

    def test_post_request_confirm_password_is_empty(self):
        self.request.method = 'POST'
        self.request.POST['old_password'] = 'admin'
        self.request.POST['new_password'] = 'admin'
        self.request.POST['conf_password'] = ''
        self.response = change_password(self.request)
        self.assertContains(self.response, 'Please enter your confirm password.')

    def test_post_request_confirm_password_not_match_with_new_password(self):
        self.request.method = 'POST'
        self.request.POST['old_password'] = 'admin'
        self.request.POST['new_password'] = 'admin'
        self.request.POST['conf_password'] = 'a'
        self.response = change_password(self.request)
        self.assertContains(self.response, 'The confirm password not match with the new password, please try again.')

    def test_post_request_new_password_the_same_as_old_password(self):
        self.request.method = 'POST'
        self.request.POST['old_password'] = 'admin'
        self.request.POST['new_password'] = 'admin'
        self.request.POST['conf_password'] = 'admin'
        self.response = change_password(self.request)
        self.assertContains(self.response, 'The new password was the same as your old password, please try again.')

    def test_post_request_wrong_old_password(self):
        self.request.method = 'POST'
        self.request.POST['old_password'] = 'wrong'
        self.request.POST['new_password'] = 'admin'
        self.request.POST['conf_password'] = 'admin'
        self.response = change_password(self.request)
        self.assertContains(self.response, 'Your old password incorrect, please try again.')        

    def test_post_request_change_password_success(self):
        self.request.method = 'POST'
        self.request.POST['old_password'] = 'max123'
        self.request.POST['new_password'] = '123456'
        self.request.POST['conf_password'] = '123456'
        self.response = change_password(self.request)
        self.assertEqual(User.objects.first().pwd, '123456')
        self.assertEqual(self.response.status_code, 302)
        self.assertEqual(self.response.url, reverse('login', args=None))
