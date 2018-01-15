from attendence.models import Punch
from secu.models import User
from attendence.tests.test_base import TestBase
from attendence.views.punch import _Punch
# index,get_list_by_filter
'''
    1. GET请求，返回的内容包含'Raymon Gen'
    2. 返回码为200
    3. 返回的内容包含'Not Normal','N/A','2016-05-17'

'''
class GetNames(TestBase):
    
    def test_get_names(self):
        user = User.objects.create(user_name='admin1',pwd='admin1',first_name='Raymon',last_name='Gen')
        request = self.request
        request.method = 'GET'
        response = _Punch.index(request)
        self.assertContains(response, 'Raymon Gen')
        self.assertEqual(response.status_code, 200)
        
    # def test_search_result_default(self):
    #     user = User.objects.create(user_name='admin1',pwd='admin1')
    #     employee = Employee.objects.create(user=user,first_name='Raymon',last_name='Gen')
    #     request = self.request
    #     request.method = 'GET'
    #     request.GET['user_name_search'] = '0'
    #     request.GET['punchtime_search_start'] = '2016-05-17'
    #     request.GET['punchtime_search_stop'] = '2016-05-17'
    #     response = get_list_by_filter(request)
    #     self.assertContains(response, 'Not Normal')
    #     self.assertContains(response, 'N/A')
    #     self.assertContains(response, '2016-05-17')
    #     self.assertEqual(response.status_code, 200)
