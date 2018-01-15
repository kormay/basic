from attendence.tests.test_base import TestBase
from django.core.urlresolvers import resolve, reverse
from django.http import HttpRequest
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.html import escape

from attendence.views.leave import approve_deny
from secu.models import User
from attendence.models import Adjustment, AdjustmentLog
from django.http.response import JsonResponse
import json


''' 
    1. operation为1时，approve
    2. operation为2时，deny

'''    
class ApproveDeny(TestBase):
    def test_post_request_approve(self):
        self.request.method = 'POST'  
        Adjustment.objects.create(
            user=User.objects.get(user_name='root'),
            adjustment_type='L',
            start_datetime='2016-01-01',
            end_datetime='2016-02-01'
        )   
        self.request.POST['id'] = Adjustment.objects.first().id
        self.request.POST['operation'] = '1'
        self.response = approve_deny(self.request)
        self.assertEqual(self.response.content.decode(), 'The leave apply has been approved/denied.') 

    def test_post_request_deny(self):
        self.request.method = 'POST'  
        Adjustment.objects.create(
            user=User.objects.get(user_name='root'),
            adjustment_type='L',
            start_datetime='2016-01-01',
            end_datetime='2016-02-01'
        )   
        self.request.POST['id'] = Adjustment.objects.first().id
        self.request.POST['operation'] = '2'
        self.response = approve_deny(self.request)
        self.assertEqual(self.response.content.decode(), 'The leave apply has been approved/denied.') 

     