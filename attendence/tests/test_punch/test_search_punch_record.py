from attendence.tests.test_base import TestBase
from attendence.models import Punch
from secu.models import User
from attendence.views.punch import _Punch
'''
    1.GET请求
    2.插入一条punch记录，并且能在返回结果中查询到
'''
class SearchAllRecord(TestBase):

    def test_search_all_record(self):
        user = User.objects.create(user_name='raymon',pwd='raymon',first_name='Raymon',last_name='Gen')
        request = self.request
        punch = Punch.objects.create(user=user,punch_date='2016-05-18', is_normal=False, IP=request.get_host())
        request.method = 'GET'
        request.GET['user_name_searchall'] = 'raymon'
        request.GET['punchdate_searchall'] = '2016-05-18'
        response = _Punch.get_all_list_by_filter(request)
        self.assertContains(response, '2016-05-18')
        self.assertContains(response, 'No')