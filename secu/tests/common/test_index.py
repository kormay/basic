from django.test import TestCase
from django.http import HttpResponse, HttpRequest
from django.core.urlresolvers import resolve
from secu.views import _Common

class TestIndex(TestCase):
    def test_root_url_resolves_to_index_view(self):
        found = resolve('/secu/')
        self.assertEqual(found.func, _Common.index)