from django.test import TestCase
from django.http import HttpResponse, HttpRequest
from django.core.urlresolvers import resolve
from secu.views import _Right
from secu.models import Right
from attendence.urls import urlpatterns
from unittest import skip

class TestInitList(TestCase):
    def test_first_init_list(self):
        attendence_count = len(urlpatterns)
        _Right.init_list()
        total = Right.objects.all().count()
        self.assertEqual(total >= attendence_count, True)