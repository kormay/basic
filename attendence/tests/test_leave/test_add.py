from attendence.tests.test_base import TestBase
from django.core.urlresolvers import resolve, reverse
from django.http import HttpRequest
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import escape

from attendence.views.leave import add
from secu.models import User
from attendence.models import Adjustment, AdjustmentLog
from django.http.response import JsonResponse
import json


''' 
    1. 如果是POST请求，传入正确的时间，申请数据成功
    2. 如果是POST请求，传入错误的时间，申请数据失败

'''    
class Add(TestBase):
    def test_post_request_add_adjustment_date_right_style(self):
        self.request.method = 'POST'
        self.request.POST['StartDate'] = '2015-01-01'
        self.request.POST['EndDate'] = '2015-02-01'


        self.response = add(self.request)
        self.assertEqual(self.response.content.decode(), 'Leave apply success') 

    def test_post_request_add_adjustment_date_wrong_style(self):
        self.request.method = 'POST'
        self.request.POST['StartDate'] = '2015-aa-01'
        self.request.POST['EndDate'] = '2015-02-bb'
        self.response = add(self.request)
        self.assertEqual(self.response.content.decode(), 'The date is not in the correct style.') 
    