from django.test import TestCase, override_settings
from django.http import HttpRequest
from secu.models import User
from attendence.models import Employee
import os

from secu.views import _Right
from attendence.views import account
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestBase(TestCase):

    # @override_settings(DATABASES={
    #     'default': {
    #         'ENGINE': 'django.db.backends.sqlite3',
    #         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    #     }
    # })
    @override_settings(RUN_TEST=1)
    def setUp(self):
        self.user = account.create_root_user()
        self.request = HttpRequest()
        self.request.META['SERVER_NAME'] = '127.0.0.1'
        self.request.META['SERVER_PORT'] = '80'
        self.request.session = {'user_name': self.user.user_name}
        # self.employee = User.objects.create(user=self.user, first_name='admin', last_name='Max', email='admin@admin.com')
        _Right.init_list()

    @override_settings(RUN_TEST=1)
    def tearDown(self):
        self.user.delete()
