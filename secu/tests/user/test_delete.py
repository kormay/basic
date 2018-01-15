from attendence.tests.test_base import TestBase
from attendence.views.employee import delete
from attendence.models import Employee
from secu.models import User
from django.core.exceptions import ObjectDoesNotExist
'''
    1. 如果是GET请求，则返回None
    2. 如果是POST请求，且PK为空，则返回'false'
    3. 如果是POST请求，且PK不为空，则返回'success'
'''


class Delete(TestBase):
    """docstring for GetList"""
    @classmethod
    def setUpTestData(cls):
        for i in range(5):
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

    def setUp(self):
        self.pk = User.objects.get(user_name='Purk3').id
        super().setUp()

    def test_get_request_delete(self):
        request = self.request
        request.method = 'GET'
        response = delete(request)
        self.assertEqual(response, None)

    def test_post_request_no_pk_delete(self):
        request = self.request
        request.method = 'POST'
        request.POST['pk'] = ''
        response = delete(request)
        self.assertEqual(response.content.decode(), 'false')

    def test_post_request_exists_pk_delete(self):
        request = self.request
        request.method = 'POST'
        request.POST['pk'] = self.pk
        print('*******************************************')
        print(self.pk)
        print('*******************************************')
        response = delete(request)
        # self.assertEqual(response.content.decode(), 'success')
        # with self.assertRaisesMessage(ObjectDoesNotExist, 'User matching query does not exist.'):
        #     User.objects.get(id=self.pk)
