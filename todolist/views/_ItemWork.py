from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from tools.ui.pager import get_record_index

from todolist.models import Item, ItemWork, Step
from secu.models import User
import json

class _ItemWork:

    def add(request):
        if request.method == 'POST':
           item = Item.objects.get(pk=request.POST['item_id'])
           instance = ItemWork()
           instance.item = item
           instance.work = request.POST['work']
           instance.minutes = int(request.POST['minutes'])
           instance.entry_user = User.objects.get(user_name=request.session.get('user_name'))
           instance.save()
           return HttpResponse(50000)   

    def delete(request):
        if request.method == 'POST':
           ItemWork.objects.get(pk=request.POST['id']).delete()
           return HttpResponse(50000)   

    def edit(request):
        if request.method == 'GET':
            instance = ItemWork.objects.get(pk=request.GET['id'])
            return JsonResponse(instance.json, safe=False)   
        elif request.method == 'POST':
            item = Item.objects.get(pk=request.POST['item_id'])
            instance = ItemWork.objects.get(pk=request.POST['id'],item=item) 
            instance.work = request.POST['work']
            instance.minutes = int(request.POST['minutes'])
            instance.entry_user = User.objects.get(user_name=request.session.get('user_name'))
            instance.save()                     
            return HttpResponse(50000)

    def list(request):
        if request.method == 'GET':
            record = get_record_index(request)
            item = Item.objects.get(pk=request.GET['item_id'])

            data = [
                        {
                            "id": ins.id,
                            "work": ins.work,  
                            "minutes": ins.minutes,
                            "user": ins.entry_user.first_name+' '+ ins.entry_user.last_name if ins.entry_user else '',
                            "entry_date": ins.entry_date 
                        } for ins in ItemWork.objects.filter(item=item)[record['start']:record['end']] 
                    ]  

            context = {
                "totalrecords": ItemWork.objects.filter(item=item).count(),
                "data": data
            }                    
            return JsonResponse(context, safe=False)

    def instance(request):
        if request.method == 'GET':
            instance = Item.objects.get(pk=request.GET['id'])

            data = instance.json
            data['step'] = instance.step.id if instance.step else ''
            data['status'] = instance.status.id if instance.status else ''
            data['person_in_charge'] = instance.person_in_charge.id if instance.person_in_charge else ''
            data['total_time'] =  instance.minutes
            data['used_total_time'] =  _ItemWork.get_used_item_total_time(instance)   
            return JsonResponse(data, safe=False)   

    def get_used_item_total_time(item):
        total_time = 0
        item_works = ItemWork.objects.filter(item=item)
        for item_work in item_works:
            total_time = total_time + item_work.minutes
        return total_time
        