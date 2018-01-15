from django.shortcuts import render
from django.http import HttpResponse

class _StartProcess(object):
    def index(request):
        context = {
            'title_text': 'Start Process'
        }
        return render(request,'workflow/start_process.html',context)

    def save(request):
        if request.method == 'POST':
            return HttpResponse('sucess')
