from django.test import TestCase
from basic.render import render_with_right_by_pyQuery
from attendence.views.account import create_root_user
from pyquery import PyQuery
from secu.models import *


class Render(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(user_name='purk')
        create_root_user()

        right_index = Right.objects.create(name='attendence.views.index', view_name='attendence.views.index')
        right_add = Right.objects.create(name='attendence.views.add', view_name='attendence.views.add')

        role_dev = Role.objects.create(name='开发', detail='随意')
        role_test = Role.objects.create(name='测试', detail='随asdfasdf意')

        RoleRight.objects.create(role=role_dev, right=right_index)
        RoleRight.objects.create(role=role_test, right=right_add)

        UserRole.objects.create(user=user, role=role_dev)

    def test_render_with_right_by_pyQuery_root(self):
        with open('basic/test/render/test_html.html', 'r') as file:
            test_str = file.readlines()
            result_str = render_with_right_by_pyQuery('root', ''.join(test_str))
            PQ = PyQuery(result_str)
            self.assertNotEqual(PQ('#test_index').outer_html(), None)
            self.assertNotEqual(PQ('#test_add').outer_html(), None)

    def test_render_with_right_by_pyQuery_other(self):
        with open('basic/test/render/test_html.html', 'r') as file:
            test_str = file.readlines()
            result_str = render_with_right_by_pyQuery('purk', ''.join(test_str))
            PQ = PyQuery(result_str)

            self.assertNotEqual(PQ('#test_index').outer_html(), None)
            self.assertEqual(PQ('#test_add').outer_html(), None)
