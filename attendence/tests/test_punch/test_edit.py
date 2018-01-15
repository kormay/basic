from datetime import datetime

from attendence.tests.test_base import TestBase
from attendence.models import Punch
from secu.models import User
from attendence.views.punch import _Punch

'''
    1. 如果是GET请求，则返回None
    2. 如果是POST请求，Not Normal, 则返回'Edit punch info success.'
    2. 如果是POST请求，Normal, 则返回'You can't edit this record.'
'''

class Edit(TestBase):
    
    @classmethod
    def setUpTestData(cls):
        for i in range(5):
            user = User()
            user.user_name = 'Raymon' + str(i)
            user.pwd = '123456'
            user.first_name = 'Raymon' + str(i)
            user.last_name = 'Gen' + str(i)
            user.email = 'rgen' + str(i) + '@maxprocessing.com'
            user.save()
            pun = Punch()
            pun.user = user
            pun.punch_date = '2016-05-16 10:00'
            if i == 3:
                pun.is_normal = True
            else:
                pun.is_normal = False
            pun.IP = '127.0.0.1'
            pun.save()

    def setUp(self):
        self.pk_normal = Punch.objects.get(id=4).id
        self.pk_not_normal = Punch.objects.get(id=2).id
        super().setUp()
        
    def test_get_request_edit(self):
        request = self.request
        request.method = 'GET'
        response = _Punch.edit(request)
        self.assertEqual(response, None)
        
    def test_post_request_notnormal_edit(self):
        request = self.request
        request.method = 'POST'
        request.POST['punch_time'] = '2016-05-16 10:20'
        request.POST['id'] = self.pk_not_normal
        response = _Punch.edit(request)
        self.assertEqual(response.content.decode(), 'Edit punch info success.')

    def test_post_request_normal_edit(self):
        request = self.request
        request.method = 'POST'
        request.POST['punch_time'] = '2016-05-16 10:20'
        request.POST['id'] = self.pk_normal
        response = _Punch.edit(request)
        self.assertEqual(response.content.decode(), "You can't edit this record.")
