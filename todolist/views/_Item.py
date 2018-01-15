from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from tools.ui.pager import get_record_index

from todolist.models import Step, Status, Item, ItemWork
from secu.models import User
import json

from attendence.decrator import *

class _Item:
    @valid_user
    def index(request):
        return render(request, 'todolist/item.html')

    def add(request):
        if  request.method == 'POST':
            item = Item()
            item.title = request.POST['title']
            item.description = request.POST['description']
            item.minutes = request.POST['minutes']
            item.save()
            return JsonResponse(item.json)
        elif  request.method == 'GET':
            return render(request, 'todolist/item_detail.html')

    def list(request):
        if request.method == 'GET':
            record = get_record_index(request)
            data = [   
                        {
                            "id": item.id, 
                            "title": item.title,
                            "step": item.step.name if item.step else ' -- ',
                            "status": item.status.name if item.status else ' -- ',
                            "person_in_charge": item.person_in_charge.first_name+' '+ item.person_in_charge.last_name if item.person_in_charge else '--',
                            "entry_date": item.entry_date                       
                        }
                        for item in Item.objects.all()[record['start']:record['end']] 
                   ]
                   
            context = {
                "totalrecords": Item.objects.all().count(),
                "data": data
            }
            return JsonResponse(context, safe=False)
    
    def instance(request):
        if request.method == 'GET':
            instance = Item.objects.get(pk=request.GET['id'])
            return JsonResponse(instance.json, safe=False)            

    def edit(request):
        if request.method == 'POST':
            item = Item.objects.get(pk=request.POST['id'])
            if request.POST['from_flag'] == 'item_work':
                step = Step.objects.get(pk=request.POST['step'])
                status = Status.objects.get(pk=request.POST['status'])
                user = User.objects.get(pk=request.POST['person_in_charge'])
                item.step = step
                item.status = status
                item.person_in_charge = user
            else:
                item.title = request.POST['title']
                item.description = request.POST['description']
                item.minutes = request.POST['minutes']
            item.save() 
            return HttpResponse(50000)
        elif request.method == 'GET':
            return render(request, 'todolist/item_detail.html')

    def delete(request):
        if request.method == 'POST':
           item = Item.objects.get(pk=request.POST['id'])
           item.delete() 
           return HttpResponse(50000)   

    def get_options(args=0):
        result, step, status, user = {}, '', '', ''

        for obj in Step.objects.all():
            step = step + obj.as_option('id', 'name')    

        for obj in Status.objects.all():
            status = status + obj.as_option('id', 'name')    

        for obj in User.objects.all():
            user = user + obj.as_option_by_two_text('id', 'first_name', 'last_name')

        result['step'] = step
        result['status'] = status
        result['user'] = user
        return result 

    def workflow(request):
        if request.method == 'GET':
            context = _Item.get_options()
            return render(request, 'todolist/item_work.html', context)