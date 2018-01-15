from django.http import HttpRequest


from django.test import TestCase

from secu.views import _Role
from secu.models import Role

'''
1. 如果是 GET 请求，则返回 None
2. 如果是POST 请求，成功添加记录后，返回信息为50000
'''
class Add(TestCase):
    def test_add_GET(self):
        request = HttpRequest()
        request.method = 'GET'
        response = _Role.add(request)
        self.assertEqual(response, None)

    def test_add_POST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['name'] = 'test'
        request.POST['detail'] = 'test detail'

        response = _Role.add(request)

        self.assertEqual(1, Role.objects.all().count(), 'fail to save.')
        self.assertEqual(response.content, b'50000')        