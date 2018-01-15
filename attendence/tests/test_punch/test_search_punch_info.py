from datetime import datetime, date, timedelta

from attendence.models import Punch
from secu.models import User
from attendence.tests.test_base import TestBase
from attendence.views.punch import _Punch
# get_list_by_filter
'''
    1. GET请求
    2. user不为空，返回码200，页面第二页包含内容'Not Normal'，'N/A',同时包含昨天的日期,今天的日期以及打卡时间
    3. user为空，返回码200，页面第二页包含内容'Not Normal'，'N/A',同时包含昨天的日期,今天的日期以及打卡时间
'''
class SearchPunchInfo(TestBase):
    
    @classmethod
    def setUpTestData(cls):
        now = datetime.now()
        cls.now_str = datetime.strftime(now,'%Y-%m-%d %H:%M:%S')
        cls.today = date.today()
        user = User.objects.create(user_name='admin1',pwd='admin1',first_name='Raymon',last_name='Gen')
        punch = Punch.objects.create(user=user,punch_date=now, is_normal=False, IP='192.168.0.1')

    def test_search_punch_info_with_user(self):
        request = self.request
        request.method = 'GET'
        request.GET['user_name_search'] = 'admin1'
        request.GET['punchtime_search_start'] = datetime.strftime(SearchPunchInfo.today - timedelta(days=18),'%Y-%m-%d')
        request.GET['punchtime_search_stop'] = datetime.strftime(SearchPunchInfo.today,'%Y-%m-%d')
        request.GET['pagesize'] = '10'
        request.GET['currentpage'] = '2'
        response = _Punch.get_list_by_filter(request)
        self.assertContains(response, 'Not Normal')
        self.assertContains(response, 'N/A')
        self.assertContains(response, datetime.strftime(SearchPunchInfo.today - timedelta(days=1),'%Y-%m-%d'))
        self.assertContains(response, datetime.strftime(SearchPunchInfo.today,'%Y-%m-%d'))
        self.assertContains(response, SearchPunchInfo.now_str)
        self.assertEqual(response.status_code, 200)

    def test_search_punch_info_with_no_user(self):
        request = self.request
        request.method = 'GET'
        request.GET['user_name_search'] = '0'
        request.GET['punchtime_search_start'] = datetime.strftime(SearchPunchInfo.today - timedelta(days=18),'%Y-%m-%d')
        request.GET['punchtime_search_stop'] = datetime.strftime(SearchPunchInfo.today,'%Y-%m-%d')
        request.GET['pagesize'] = '10'
        request.GET['currentpage'] = '2'
        response = _Punch.get_list_by_filter(request)
        self.assertContains(response, 'Not Normal')
        self.assertContains(response, 'N/A')
        self.assertContains(response, datetime.strftime(SearchPunchInfo.today - timedelta(days=1),'%Y-%m-%d'))
        self.assertContains(response, datetime.strftime(SearchPunchInfo.today,'%Y-%m-%d'))
        self.assertContains(response, SearchPunchInfo.now_str)
        self.assertEqual(response.status_code, 200)