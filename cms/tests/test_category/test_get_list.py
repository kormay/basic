from django.test import TestCase
from django.http import HttpRequest

from cms.views.category import _Category
from cms.models import Category

class Getlist(TestCase):
    @classmethod
    def setUpTestData(cls):
        for i in range(5):
            category = Category()
            category.code = 'raymon' + str(i)
            category.title = 'raymon' + str(i)
            category.save()

    def test_get_request_get_list(self):
        request = HttpRequest()
        request.method = 'GET'
        response = _Category.get_list(request)
        self.assertContains(response, 'raymon1')
        self.assertContains(response, 'raymon3')
        self.assertEqual(response.status_code, 200)

    def test_post_request_get_list(self):
        request = HttpRequest()
        request.method = 'POST'
        response = _Category.get_list(request)
        self.assertEqual(response, None)