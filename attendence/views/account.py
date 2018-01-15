import time, datetime, uuid
from django.core import serializers
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.urlresolvers import reverse

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from attendence.models import Punch
from attendence.decrator import *
from django.views.decorators.csrf import csrf_exempt 
from secu.models import User

# Create your views here.
def login(request):
    create_root_user()
    context = None
    if request.method == 'POST':
        user_name = request.POST['user_name']
        pwd = request.POST['pwd']
        error_message = ''

        user = User.objects.filter(user_name=user_name, pwd=pwd)
        if user.count() == 0:
            error_message = 'Username or password is incorrect.'
        context = {
            'error_message': error_message,
        }

        if error_message == '':
            request.session['user_name'] = user_name
            punch(request)
            return HttpResponseRedirect(reverse('attendence:index', args=None))

    return render(request, 'attendence/login.html', context)

def logout(request):
    request.session.clear()
    return HttpResponseRedirect(reverse('login', args=None))   

@valid_user
def index(request):
    return render(request, 'attendence/index.html', {'title_text': 'Attendence System'})

@valid_user
def change_password(request):
    if request.method == 'GET':
        return render(request, 'attendence/change_password.html', {'title_text': '修改密码'})
    elif request.method == 'POST': 
        user = User.objects.filter(user_name=request.session.get('user_name'))
        current_old_password = user[0].pwd

        if request.POST.get('old_password','') == '':
            return render(request, 'attendence/change_password.html', {'message': 'Please enter your old password.'}) 
        elif request.POST.get('new_password','') == '':
            return render(request, 'attendence/change_password.html', {'message': 'Please enter your new password.'}) 
        elif request.POST.get('conf_password','') == '':
            return render(request, 'attendence/change_password.html', {'message': 'Please enter your confirm password.'}) 
        elif request.POST.get('conf_password','') != request.POST.get('new_password',''):
            return render(request, 'attendence/change_password.html', {'message': 'The confirm password not match with the new password, please try again.'}) 
        elif request.POST.get('new_password','') == request.POST.get('old_password',''):
            return render(request, 'attendence/change_password.html', {'message': 'The new password was the same as your old password, please try again.'}) 
        elif request.POST.get('old_password','') != current_old_password:
            return render(request, 'attendence/change_password.html', {'message': 'Your old password incorrect, please try again.'})     
        else:
            user.update(pwd=request.POST.get('new_password'))
            return HttpResponseRedirect(reverse('login', args=None))
           
@valid_user
@csrf_exempt
def check_old_password(request):
    if request.method == 'POST':
        user = User.objects.get(user_name=request.session.get('user_name'))
        message = ''
        if(user.pwd != request.POST.get('old_password')):
            message = 'Your old password incorrect, please try again.'
        return HttpResponse(message)

def punch(request):
    user_name = request.session.get('user_name')
    ip = request.get_host()
    user = User.objects.filter(user_name=user_name)[0]
    Punch.objects.create(user=user, IP=ip, entry_user=user)  

def create_root_user():
    from basic.config import ROOTUSER     
    if User.objects.filter(user_name=ROOTUSER['name']).count() == 0:
        root = User()
        root.user_name = ROOTUSER['name']
        root.pwd = ROOTUSER['password']
        root.save()
    
    return User.objects.get(user_name=ROOTUSER['name'])        



