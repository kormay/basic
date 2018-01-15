from django.core import serializers
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from basic.render import render
from attendence.models.Employee import Employee
from attendence.decrator import *
from django.core.mail import EmailMultiAlternatives
from django.core.mail import send_mail
from secu.models import User
from secu.models.validator import Validator
from django.db import transaction
import logging


@valid_user
def index(request):
    context = {
        'title_text': 'Validator'
    }
    return render(request, 'Validator.html', context, validator=(Validator.validator,))


@valid_user
def get_list(request):
    if request.method == 'GET':
        condition_obj = {
            "currentpage": int(request.GET.get("currentpage", 1)),
            "pagesize": int(request.GET.get("pagesize", 0))
        }

        employees = Employee.objects.all().order_by('user__user_name')[
            (condition_obj['currentpage'] - 1) * condition_obj['pagesize']: condition_obj['currentpage'] * condition_obj['pagesize']
        ]
        data = [{
            "rownum": index + 1,
            "user_id": employee.user.id,
            "first_name": employee.first_name,
            "user_name": employee.user.user_name,
            "last_name": employee.last_name,
            "email": employee.email
        } for index, employee in enumerate(employees)]

        total = Employee.objects.all().count()

        json_result = {"totalrecords": total, "data": data}
        return JsonResponse(json_result)


@valid_user
@transaction.atomic
def add(request):
    if request.method == 'POST':
        user = User()
        user.user_name = request.POST.get("user_name", '')
        user.pwd = '123456'
        user.save()
        emp = Employee()
        emp.user = user
        emp.first_name = request.POST.get("first_name", '')
        emp.last_name = request.POST.get("last_name", '')
        emp.email = request.POST.get("email", '')
        emp.save()
        return HttpResponse("success")


@valid_user
@transaction.atomic
def edit(request):
    if request.method == 'POST':
        pk = request.POST.get("user_id", '')
        if pk == '':
            return HttpResponse("false")
        emp = User.objects.get(pk=pk).employee
        emp.first_name = request.POST.get("first_name", '')
        emp.last_name = request.POST.get("last_name", '')
        emp.email = request.POST.get("email", '')
        emp.save()
        return HttpResponse("success")


@valid_user
@transaction.atomic
def delete(request):
    if request.method == 'POST':
        user_id = request.POST.get("pk", '')
        if user_id == '':
            return HttpResponse('false')
        user = User.objects.filter(pk=id)
        emp = Employee.objects.filter(user=user)
        print(emp[0])
        # emp.delete()
        # user.delete()
        # return HttpResponse("success")
