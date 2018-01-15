from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from todolist.models import Step, Status
from tools.ui.pager import get_record_index

class _Step:
    def index(request):
        return render(request, 'todolist/step.html')

    def add(request):
        if request.method == 'POST':
            item = Step()
            item.name = request.POST['name']
            item.description = request.POST['description']
            item.order = request.POST.get('order', 0)
            item.save()
            return HttpResponse(50000)

    def list(request):
        if request.method == 'GET':
            record = get_record_index(request)
            total_records = Step.objects.all().count()
            li = Step.objects.all()[record['start']:record['end']]

            data = [ item.json for item in li ]
            context = {
                "totalrecords": total_records,
                "data": data
            }
            return JsonResponse(context, safe=False)

    def edit(request):
        if request.method == 'POST':
           item = Step.objects.get(pk=request.POST['id'])
           item.name = request.POST['name']
           item.description = request.POST['description']
           item.save() 
           return HttpResponse(50000)
        elif request.method == 'GET':
            item = Step.objects.get(pk=request.GET['id'])
            return JsonResponse(item.json) 

    def delete(request):
        if request.method == 'POST':
           item = Step.objects.get(pk=request.POST['id'])
           item.delete() 
           return HttpResponse(50000)     

    

                         

