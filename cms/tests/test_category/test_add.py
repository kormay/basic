from django.test import TestCase
from django.http import HttpRequest

from cms.views.category import _Category
from cms.models import Category

class Add(TestCase):
    def test_get_request_add(self):
        request = HttpRequest()
        request.method = 'GET'
        response = _Category.add(request)
        self.assertEqual(response, None)

    def test_post_request_add_new(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['category'] = 'new category'
        response = _Category.add(request)
        self.assertEqual(response.content.decode(),'成功添加。')

    def test_post_request_add_exist_category(self):
        category = Category()
        category.code = 'old category'
        category.title = 'old category'
        category.save()
        request = HttpRequest()
        request.method = 'POST'
        request.POST['category'] = 'old category'
        response = _Category.add(request)
        self.assertEqual(response.content.decode(),'类别"old category"已经存在。')