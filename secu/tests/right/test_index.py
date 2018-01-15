from django.test import TestCase
from django.http import HttpResponse, HttpRequest
from django.core.urlresolvers import resolve
from secu.views import _Right
from unittest import skip

class TestIndex(TestCase):
    @skip
    def test_root_url_resolves_to_index_view(self):
        found = resolve('/secu/right/')
        self.assertEqual(found.func, _Right.index)
