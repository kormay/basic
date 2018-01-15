from django.core import serializers
from workflow.models import ProcessTemplate, StepTemplate, AuthorTemplate, RelationTemplate
from django.test import TestCase
from django.http import HttpRequest, HttpResponse
from workflow.views.define_process import _DefineProcess
import datetime
import json


class ProcessDefinition(TestCase):

    def test_save_process_template(self):
        '''考虑用serizlizers.deserialize反序列化为对应的可以直接save到数据库的对象，
        但是其不是根据给定数据源来序列化sql的，而是根据model的列来生成sql,数据源没有传递的值就赋值为null,
        不符合我只需更新部分字段的要求'''
        request = HttpRequest()
        request.method = 'POST'
        request.POST['data'] = '''{"process_info": {"id": "", "name": "test", "title": "test frist process", "form_source": "test.xml", "data_source": "test.html"}, "steps": [{"name": "Start", "order": "1", "coordinate_x": "420px", "coordinate_y": "50px", "author": [{"name": "", "value": "", "category": ""}] }, {"name": "End", "order": "99", "coordinate_x": "420px", "coordinate_y": "250px", "author": [{"name": "", "value": "", "category": ""}] }, {"name": "End", "order": "99", "coordinate_x": "420px", "coordinate_y": "250px", "author": [{"name": "", "value": "", "category": ""}] }], "relations": [{"relation": "1_99"}] }'''

        response = _DefineProcess.save(request)
        print(response)
        print(ProcessTemplate.objects.all())
        print(StepTemplate.objects.all())
        print(AuthorTemplate.objects.all())
        print(RelationTemplate.objects.all())

    def test_foreignkey(self):
        pt = ProcessTemplate()
        pt.name = 'test'
        pt.title = 'test first process'
        pt.save()
        at = AuthorTemplate()
        at.category = '01'
        at.value = 'asdfadsf'

        st = StepTemplate()
        st.name = 'start'
        st.order = 1
        st.process = pt
        st.coordinate_x = 120.5
        st.coordinate_y = 230.1
        st.save()

        st = StepTemplate.objects.get(name='start')
        print(StepTemplate.objects.get(name='start'))
        print(st.process)
        # print(ProcessTemplate.objects.get(name='test'))
        # pt.delete()
        # print(StepTemplate.objects.get(name='start'))
