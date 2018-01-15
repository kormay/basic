from attendence.tests.test_base import TestBase
from attendence.views.employee import add
from attendence.models import Employee

'''
    1. 如果是GET请求，则返回None
    2. 如果是POST请求,且参数不为空，则返回'success'
'''


class Add(TestBase):
    """docstring for Add"""

    def test_get_request_add(self):
        request = self.request
        request.method = 'GET'
        response = add(request)
        self.assertEqual(response, None)

    def test_post_request_add(self):
        request = self.request
        request.method = 'POST'
        request.POST['user_name'] = 'Purk'
        request.POST['first_name'] = 'Purk'
        request.POST['last_name'] = 'Wu'
        request.POST['email'] = 'pwu@maxprocessing.com'
        response = add(request)
        self.assertEqual(response.content.decode(), 'success')
        employee = Employee.objects.get(user__user_name='Purk')
        self.assertNotEqual(employee, None)
