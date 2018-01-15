from secu.models import Role, Right, RoleRight, User, UserRole
from django.http import HttpResponse, JsonResponse
# from django.shortcuts import render
from basic.render import render
from tools.ui.pager import get_record_index
from django.core.urlresolvers import reverse
from attendence.decrator import *
import json


class _User:

    @valid_user
    def index(request):
        return render(request, 'secu/user.html', validator=(User.validator, Right.validator))

    @staticmethod
    @valid_user
    def list(request):
        if request.method == 'GET':
            record = get_record_index(request)
            total_records = User.objects.all().count()
            li = User.objects.all()[record['start']:record['end']]

            data = [
                {
                    "id": item.id,
                    "user_name": item.user_name,
                    "first_name": item.first_name,
                    "last_name": item.last_name,
                    "email": item.email,
                    "url": reverse('secu:user_role_list', kwargs={'user_id': item.id})
                }
                for item in li
            ]

            context = {
                "totalrecords": total_records,
                "data": data
            }
            return JsonResponse(context, safe=False)

    @valid_user
    def get_role_list_by_user(request, user_id):
        if request.method == 'GET':
            user = User.objects.get(id=user_id)
            record = get_record_index(request)

            user_role_list = [item.role.id for item in UserRole.objects.filter(user=user)]

            total_records = Role.objects.all().count()
            li = Role.objects.all()[record['start']:record['end']]

            data = [
                {
                    "id": item.id,
                    "name": item.name,
                    "detail": item.detail,
                    "own": 'checked' if item.id in user_role_list else '',
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
    def add_delete_role_to_user(request):
        if request.method == 'POST':
            role = Role.objects.get(id=request.POST['role_id'])
            user = User.objects.get(id=request.POST['user_id'])
            operation = request.POST['operation']
            if operation == 'add':
                UserRole.objects.create(role=role, user=user)
            elif operation == 'delete':
                RoleRight.objects.filter(role=role, user=user).delete()
            return HttpResponse(50000)

    @staticmethod
    @valid_user
    def add(request):
        if request.method == 'POST':
            user = User()
            user.user_name = request.POST['user_name']
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.pwd = '123456'
            user.save()
            return HttpResponse(50000)

    @staticmethod
    @valid_user
    def delete(request):
        if request.method == 'POST':
            user = User.objects.get(id=request.POST['user_id'])
            user.delete()
            return HttpResponse(50000)

    @staticmethod
    @valid_user
    def edit(request):
        if request.method == 'POST':
            user = User.objects.get(id=request.POST['user_id'])
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()
            return HttpResponse(50000)
        elif request.method == 'GET':
            print(request.GET['user_id'])
            user = User.objects.get(id=request.GET['user_id'])

            return JsonResponse(user.json, safe=False)
