import uuid

from django.db import models
from datetime import datetime
from .Root import Root


class User(Root):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_name = models.CharField(max_length=30)
    pwd = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    email = models.EmailField(default='')
    entry_user = models.ForeignKey('self', on_delete=models.CASCADE, related_name="entry_user_self", null=True)

    validator = {
        'User_user_name': {'type':'string', 'max':30, 'min':0, 'msg':''},
        'User_pwd': {'type':'string', 'max':50, 'min':1, 'msg':''},
        'User_first_name': {'type':'string', 'max':50, 'min':0, 'msg':''},
        'User_last_name': {'type':'string', 'max':50, 'min':0, 'msg':''},
        'User_email': {'type':'email', 'max':254, 'min':0, 'msg':''}
    }
    
    @property
    def full_name(self):
        return self.last_name + self.first_name
    
