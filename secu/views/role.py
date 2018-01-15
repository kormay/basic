from secu.models import Role, Right, RoleRight
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from tools.ui.pager import get_record_index
from django.core.urlresolvers import reverse
from attendence.decrator import *

class _Role:
    @valid_user
    def index(request):
        return render(request, 'secu/role.html')

    @staticmethod
    @valid_user     
    def list(request):
        if request.method == 'GET':
            record = get_record_index(request)
            total_records = Role.objects.all().count()
            li = Role.objects.all()[record['start']:record['end']]

            data = [
                        {
                         "id": item.id,   
                         "name": item.name, 
                         "detail": item.detail,
                         "url": reverse('secu:role_right_list', kwargs={'role_id':item.id})
                        } 
                        for item in li
                   ]

            context = {
                "totalrecords": total_records,
                "data": data
            }
            return JsonResponse(context, safe=False)

    @staticmethod
    @valid_user     
    def single(request):
        if request.method == 'GET':
            instance = Role.objects.get(id=request.GET['role_id'])

            data = {
                "id": instance.id,
                "name": instance.name,
                "detail": instance.detail
            }

            context = {
                "code": 50000,
                "data": data
            }
            return JsonResponse(context, safe=False)            

    @valid_user        
    def get_right_list_by_role(request, role_id):
        if request.method == 'GET':
            role = Role.objects.get(id=role_id)
            record = get_record_index(request)

            role_right_list = [item.right.id for item in RoleRight.objects.filter(role=role)]

            total_records = Right.objects.all().count()
            li = Right.objects.all()[record['start']:record['end']]

            data = [
                        {
                         "id": item.id,   
                         "name": item.name, 
                         "detail": item.detail,
                         "own": 'checked' if item.id in role_right_list else '',
                        } 
                        for item in li
                   ]

            context = {
                "totalrecords": total_records,
                "data": data
            }
            return JsonResponse(context, safe=False)    
            
    @staticmethod        
    @valid_user
    def add_delete_right_to_role(request):
        if request.method == 'POST':
            role = Role.objects.get(id=request.POST['role_id'])
            right = Right.objects.get(id=request.POST['right_id'])
            operation = request.POST['operation']
            if operation == 'add':
                RoleRight.objects.create(role=role, right=right)
            elif operation == 'delete':
                RoleRight.objects.filter(role=role, right=right).delete()
            return HttpResponse(50000)

    @valid_user        
    def add(request):
        if request.method == 'POST':
            role = Role()
            role.name = request.POST['name']
            role.detail = request.POST['detail']
            role.save()
            return HttpResponse(50000)
    def delete(request):
        if request.method == 'POST':
            role = Role.objects.get(id=request.POST['role_id'])
            UserRole.objects.filter(role=role).delete()
            RoleRight.objects.filter(role=role).delete()
            role.delete()
            return HttpResponse(50000)

    def edit(request):
        if request.method == 'POST':
            role = Role.objects.get(id=request.POST['role_id'])
            role.name = request.POST['name']
            role.detail = request.POST['detail']
            role.save()
            return HttpResponse(50000)       

