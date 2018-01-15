from django.db import models
from datetime import datetime
from .Root import Root


class Validator(Root):

    name = models.CharField(max_length=30)
    pwd = models.CharField(max_length=50)
    email = models.EmailField(default='')
    url = models.CharField(max_length=100)
    money = models.FloatField(max_length=15)
    age = models.DecimalField(max_digits=200)
    birthday = models.DateField()
    modification_date = models.DateTimeField()
    reg = models.CharField(max_length=200)

    validator = {
        'Validator_name': {'type': 'string', 'max': 30, 'min': 0, 'msg': '名字的长度必须在30以内', 'req': 1},
        'Validator_pwd': {'type': 'password', 'max': 50, 'min': 0, 'msg': '密码必须是数字、字母和字符', 'req': 1},
        'Validator_email': {'type': 'email', 'max': 254, 'min': 0, 'msg': 'email格式有误', 'req': 1},
        'Validator_url': {'type': 'url', 'max': 100, 'min': 0, 'msg': 'url格式有误', 'req': 1},
        'Validator_money': {'type': 'money', 'max': 150000000, 'min': -1000, 'msg': '必须是小于150000000和大于-1000的金额', 'req': 1},
        'Validator_age': {'type': 'decimal', 'max': 200, 'min': 0, 'msg': '必须是0-200以内的整数', 'req': 1},
        'Validator_birthday': {'type': 'date', 'max': '2100-05-06', 'min': '1999-01-01', 'msg': '必须是1999-01-01到2100-05-06之间的日期', 'req': 1},
        'Validator_modification_date': {'type': 'datetime', 'max': '2100-05-06 12:05:03', 'min': '1999-01-01 13:05:03', 'msg': '必须是1999-01-01 13:05:03到2100-05-06 12:05:03之间的日期'},
        'Validator_reg': {'type': 'reg', 'max': 200, 'min': 0, 'msg': '', 'req': 1}
    }
