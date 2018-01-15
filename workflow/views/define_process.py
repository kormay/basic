from django.shortcuts import render
from django.http import HttpResponse
from workflow.models.ProcessTemplate import ProcessTemplate
from workflow.models.StepTemplate import StepTemplate
from workflow.models.AuthorTemplate import AuthorTemplate
from workflow.models.RelationTemplate import RelationTemplate
from workflow.models.ProcessCategory import ProcessCategory
from django.views.decorators.csrf import csrf_exempt 

from django.db import transaction
import json


class _DefineProcess(object):

    def index(request):
        category_options = ''
        for process_category in ProcessCategory.objects.filter(level=1):
            category_options += '<option value="{0}">{1}</option>'.format(process_category.code, process_category.name)
        context = {
            'title_text': 'Process Definition',
            'category': category_options
        }
        return render(request, 'workflow/define_process_templates.html', context)

    @transaction.atomic
    @csrf_exempt
    def save(request):
        if request.method == 'POST':
            data = request.POST.get('data', '')
            if data == '':
                return HttpResponse('false')
            process_json = json.loads(data)
            process_info = process_json['process_info']
            if process_info.get('id', '') != '':
                ProcessTemplate.objects.get(pk=process_info.get('id', '')).delete()
            process_info.pop('id', '')
            process = ProcessTemplate.objects.create(**process_info)
            step_dict = {}
            for step_json in process_json['steps']:
                authors_json = step_json['author']
                step_json.pop('author')
                step = StepTemplate(**step_json)
                step.process = process
                step.save()
                step_dict[str(step.order)] = step

                for author_json in authors_json:
                    Author = AuthorTemplate(**author_json)
                    Author.process = process
                    Author.step = step
                    Author.save()
            for relation_json in process_json['relations']:
                relation_list = relation_json['relation'].split('_')
                relation = RelationTemplate()
                relation.process = process
                relation.from_step = step_dict[relation_list[0]]
                relation.to_step = step_dict[relation_list[1]]
                relation.save()

            return HttpResponse('sucess')
