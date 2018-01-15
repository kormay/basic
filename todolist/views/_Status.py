from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from todolist.models import Status
from tools.ui.pager import get_record_index

class _Status:
    
    def index(request):
        return render(request, 'todolist/status.html')

    def add(request):
        if request.method == 'POST':
            item = Status()
            item.name = request.POST['name']
            item.description = request.POST['description']
            item.order = request.POST.get('order', 0)
            item.save()
            return HttpResponse(50000)

    def list(request):
        if request.method == 'GET':
            record = get_record_index(request)
            data = [ item.json for item in Status.objects.all()[record['start']:record['end']] ]
            context = {
                "totalrecords": Status.objects.all().count(),
                "data": data
            }
            return JsonResponse(context, safe=False)

    def edit(request):
        if request.method == 'POST':
           item = Status.objects.get(pk=request.POST['id'])
           item.name = request.POST['name']
           item.description = request.POST['description']
           item.save() 
           return HttpResponse(50000)
        elif request.method == 'GET':
            item = Status.objects.get(pk=request.GET['id'])
            return JsonResponse(item.json) 

    def delete(request):
        if request.method == 'POST':
           item = Status.objects.get(pk=request.POST['id'])
           item.delete() 
           return HttpResponse(50000)       

