from attendence.tests.test_base import TestBase
from django.http import HttpRequest, JsonResponse
from attendence.views.employee import get_list
from attendence.models import Employee
from secu.models import User
import json

'''
    1. 如果是GET请求，则返回JsonResponse对象的数据
    2. 如果是POST请求，则返回None
'''

class GetList(TestBase):
    """docstring for GetList"""
    @classmethod
    def setUpTestData(cls):
        for i in range(25):
            user = User()
            user.user_name = 'Purk' + str(i)
            user.pwd = '123456'
            user.save()
            emp = Employee()
            emp.user = user
            emp.first_name = 'Purk' + str(i)
            emp.last_name = 'Wu' + str(i)
            emp.email = 'pwu' + str(i) + '@maxprocessing.com'
            emp.save()

    def test_post_request_get_list(self):
        request = self.request
        request.method = 'POST'
        response = get_list(request)
        self.assertEqual(response, None)

    def test_get_request_get_list(self):
        request = self.request
        request.method = 'GET'
        request.GET['currentpage'] = 1
        request.GET['pagesize'] = 10
        response = get_list(request)
        employeeJson = json.loads(response.content.decode())
        self.assertEqual(len(employeeJson['data']), 10)
        # 分页
        request.GET['currentpage'] = 2
        request.GET['pagesize'] = 10
        response = get_list(request)
        employeeJson = json.loads(response.content.decode())        
        self.assertEqual(len(employeeJson['data']), 10)
        # 分页
        request.GET['currentpage'] = 3
        request.GET['pagesize'] = 10
        response = get_list(request)
        employeeJson = json.loads(response.content.decode())
        self.assertEqual(len(employeeJson['data']), 6)
