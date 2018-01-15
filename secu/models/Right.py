import uuid

from django.db import models
from datetime import datetime
from .Root import Root

class Right(Root):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)    
    name = models.CharField(max_length=200)
    detail = models.CharField(max_length=8000)
    view_name = models.CharField(max_length=200)
    pattern = models.CharField(max_length=200)
    selector = models.CharField(max_length=200)   

    validator = {
        'Right_name': {'type':'string', 'max':30, 'min':0, 'msg':''},
        'Right_detail': {'type':'string', 'max':50, 'min':1, 'msg':''},
        'Right_view_name': {'type':'string', 'max':50, 'min':0, 'msg':''},
        'Right_pattern': {'type':'string', 'max':50, 'min':0, 'msg':''},
        'Right_selector': {'type':'email', 'max':254, 'min':0, 'msg':''}
    }