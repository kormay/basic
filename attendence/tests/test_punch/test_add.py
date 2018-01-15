from datetime import datetime, timedelta, date

from attendence.tests.test_base import TestBase
from secu.models import User
from attendence.models import Punch
from attendence.views.punch import _Punch

'''
    1. 如果是GET请求，则返回None
    2. 如果是POST请求,且参数不为空，则返回'Add punch info success.'
'''

class Add(TestBase):

    def test_get_request_add(self):
        request = self.request
        request.method = 'GET'
        response = _Punch.add(request)
        self.assertEqual(response, None)
        
    def test_post_request_add(self):
        user = User.objects.create(user_name='raymon',pwd='raymon', first_name='Raymon',last_name='Gen')
        request = self.request
        request.method = 'POST'
        request.POST['user_name'] = 'raymon'
        yesterday = date.today() - timedelta(days=1)
        request.POST['punch_time'] = datetime.strftime(yesterday,'%Y-%m-%d %H:%M')
        response = _Punch.add(request)
        self.assertEqual(response.content.decode(), 'Add punch info success.')
        self.assertEqual(User.objects.count(), 2)