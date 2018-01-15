from django.db import models
from datetime import datetime


class Root(models.Model):
    entry_date = models.DateTimeField(auto_now=True)

    @property
    def json(self):
        data = {}
        for key, value in self.__dict__.items():
            data[key] = str(value)
        return data

    def as_option(self, value, text, selected=''):
        return '<option value="{}" {}>{}</option>'.format(getattr(self, value), selected, getattr(self, text))

    def as_option_by_two_text(self, value, text1, text2, selected=''):
        return '<option value="{}" {}>{} {}</option>'.format(getattr(self,value), selected, getattr(self,text1), getattr(self, text2))

    class Meta:
        abstract = True

    validator = {}

    @classmethod
    def validate(cls, **kwargs):
        for key, value in kwargs.items():
            field = cls.validator.get(key, None)
            if field:
                rule = field.get('type', 'default')
                if not cls.validator_rule.get(rule, cls.validator_default)(value, **cls.validator[key]):
                    return False

    @classmethod
    def validator_string(cls, v, **kwargs):
        print(v)
        [print(key + ':' + str(value)) for key, value in kwargs.items()]

    @classmethod
    def validator_email(cls, v, **kwargs):
        pass

    @classmethod
    def validator_reg(cls, v, **kwargs):
        return True

    @classmethod
    def validator_default(cls, v, **kwargs):
        return True

    validator_rule = {
        'string': validator_string,
        'email': validator_email,
        'reg': validator_reg,
        'default': validator_default
    }
