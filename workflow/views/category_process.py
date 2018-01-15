from django.shortcuts import render
from workflow.models.ProcessCategory import ProcessCategory


class _CategoryProcess(object):

    def index(request):
        content = {
        }
        return render(request, 'workflow/category_process.html', content)
