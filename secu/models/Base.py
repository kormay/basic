from django.db import models
from datetime import datetime
from .User import User
from .Root import Root

class Base(Root):
    entry_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(app_label)s_%(class)s", null=True)
    
    @property
    def json(self):
        data = {}
        for key, value in self.__dict__.items():
            data[key] = str(value)
        return data    

    def as_option(self, value, text, selected=''):
        return '<option value="{}" {}>{}</option>'.format(getattr(self,value), selected, getattr(self,text))

    class Meta:
        abstract = True

