from attendence.tests.test_base import TestBase
from django.core.urlresolvers import resolve, reverse
from django.http import HttpRequest
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import escape

from attendence.views.leave import get_list
from secu.models import User
from attendence.models import Adjustment, AdjustmentLog
from django.http.response import JsonResponse
import json


''' 
    1. 如果是GET请求，初始化页面, 返回200
    2. 如果没有adjustment, 返回空数据
    3. 如果没有adjustment, 返回的status为Waiting, 显示操作按钮
    4. 如果有被approved的数据， 返回status为Approved， 隐藏操作按钮
    5. 如果有被deny的数据， 返回status为Denied， 隐藏操作按钮

'''    
class GetList(TestBase):
    def test_get_request_render_to_leave_page(self):
        self.request.method = 'GET'
        self.response = get_list(self.request)
        self.assertEqual(self.response.status_code, 200) 

    def test_get_request_no_adjustment(self):
        self.request.method = 'GET' 
        self.request.GET['currentpage'] = 1
        self.request.GET['pagesize'] = 10
        self.response = get_list(self.request) 
        json_obj = json.loads(self.response.content.decode())
        self.assertEqual(json_obj['totalrecords'], 0)
        self.assertEqual(json_obj['data'], [])

    def test_get_request_no_adjustment_log(self):
        self.request.method = 'GET' 
        self.request.GET['currentpage'] = 1
        self.request.GET['pagesize'] = 10

        Adjustment.objects.create(
            user = User.objects.get(user_name='root'),
            adjustment_type='L',
            start_datetime='2016-01-01',
            end_datetime='2016-02-01'
        ) 
        self.response = get_list(self.request) 
        self.assertEqual(self.response.status_code, 200) 
        json_obj = json.loads(self.response.content.decode()) 
        self.assertEqual(json_obj['data'][0].get('status'), 'Waiting')
        self.assertEqual(json_obj['data'][0].get('btn_class'), 'show_inline')

    def test_get_request_show_approve(self):
        self.request.method = 'GET' 
        self.request.GET['currentpage'] = 1
        self.request.GET['pagesize'] = 10
        Adjustment.objects.create(
            user = User.objects.get(user_name='root'),
            adjustment_type='L',
            start_datetime='2016-01-01',
            end_datetime='2016-02-01'
        ) 
        AdjustmentLog.objects.create(
            adjustment = Adjustment.objects.first(),
            operation = 1           
        )
        self.response = get_list(self.request) 
        self.assertEqual(self.response.status_code, 200) 
        json_obj = json.loads(self.response.content.decode()) 
        self.assertEqual(json_obj['data'][0].get('status'), 'Approved')
        self.assertEqual(json_obj['data'][0].get('btn_class'), 'hide')

    def test_get_request_show_deny(self):
        self.request.method = 'GET' 
        self.request.GET['currentpage'] = 1
        self.request.GET['pagesize'] = 10
        Adjustment.objects.create(
            user = User.objects.get(user_name='root'),
            adjustment_type='L',
            start_datetime='2016-01-01',
            end_datetime='2016-02-01'
        ) 
        AdjustmentLog.objects.create(
            adjustment = Adjustment.objects.first(),
            operation = 2           
        )
        self.response = get_list(self.request) 
        self.assertEqual(self.response.status_code, 200) 
        json_obj = json.loads(self.response.content.decode()) 
        self.assertEqual(json_obj['data'][0].get('status'), 'Denied')
        self.assertEqual(json_obj['data'][0].get('btn_class'), 'hide')

    