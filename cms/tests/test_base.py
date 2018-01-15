from django.test import TestCase
from django.http import HttpRequest

class TestBase(TestCase):
    def setUp(self):
        self.request  = HttpRequest()