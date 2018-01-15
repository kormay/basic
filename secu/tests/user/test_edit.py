from attendence.tests.test_base import TestBase
from attendence.views.employee import edit
from attendence.models import Employee
from secu.models import User
'''
    1. 如果是GET请求，则返回None
    2. 如果是POST请求，且user_id为空，则返回'false'
    3. 如果是POST请求，且参数不为空，则返回'success'
'''


class Edit(TestBase):
    """docstring for Edit"""

    @classmethod
    def setUpTestData(cls):
        usertemp = User()
        usertemp.user_name = 'Purk'
        usertemp.pwd = '123456'
        usertemp.save()
        emp = Employee()
        emp.user = usertemp
        emp.first_name = 'Purk'
        emp.last_name = 'Wu'
        emp.email = 'pwu@maxprocessing.com'
        emp.save()

    def setUp(self):
        self.user_id = User.objects.get(user_name='Purk').id
        super().setUp()

    def test_get_request_edit(self):
        request = self.request
        request.method = 'GET'
        response = edit(request)
        self.assertEqual(response, None)

    def test_post_request_no_user_id_edit(self):
        request = self.request
        request.method = 'POST'
        request.POST['user_id'] = ''
        response = edit(request)
        self.assertEqual(response.content.decode(), 'false')

    def test_post_request_exists_user_id_edit(self):
        request = self.request
        request.method = 'POST'
        request.POST['user_id'] = self.user_id
        request.POST['first_name'] = 'Make'
        request.POST['last_name'] = 'Xiao'
        request.POST['email'] = 'xmake@maxprocessing.com'
        response = edit(request)
        self.assertEqual(response.content.decode(), 'success')
        emp = Employee.objects.get(user_id=self.user_id)
        self.assertEqual(emp.first_name, 'Make')        
