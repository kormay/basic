from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from attendence.models.EmployeeIP import EmployeeIP
from django.db.utils import IntegrityError
from attendence.decrator import valid_user
from secu.models import User


class IP(object):

    @staticmethod
    @valid_user
    def index(request):
        users = User.objects.all()
        user_list = [{"user_name": user.user_name, "name": user.first_name + ' ' + user.last_name} for user in users]

        context = {
            'title': 'IP Management',
            'userlist': user_list,
        }

        return render(request, 'attendence/ip_manage.html', context)

    @staticmethod
    @valid_user
    def get_list(request):
        if request.method == 'GET':
            page_size = int(request.GET.get('pagesize', 10))
            start_index = (int(request.GET.get('currentpage', 1)) - 1) * page_size
            start_index = 0 if start_index < 0 else start_index
            end_index = start_index + page_size

            total_records = EmployeeIP.objects.all().count()
            employee_ips = EmployeeIP.objects.all()[start_index:end_index]
            data = [{"name": eip.user.first_name + ' ' + eip.user.last_name, "ip": eip.IP} for eip in employee_ips]

            context = {
                "totalrecords": total_records,
                "data": data
            }
            return JsonResponse(context, safe=False)

        return render(request, 'attendence/login.html', '')

    @staticmethod
    @valid_user
    def add(request):
        if request.method == 'POST':
            ip = request.POST.get('ip', None)
            if EmployeeIP.objects.filter(IP=ip).count() == 0:
                EmployeeIP.objects.create(
                    IP=ip,
                    user=User.objects.get(user_name=request.POST.get('user_name', None)),
                    entry_user=User.objects.get(user_name=request.session.get('user_name', None))
                )
            else:
                return HttpResponse(0)
            return HttpResponse(1)

        return render(request, 'attendence/login.html', '')

    @staticmethod
    @valid_user
    def delete(request):
        if request.method == 'POST':
            ip = request.POST.get('ip', None)
            try:
                result = EmployeeIP.objects.get(IP=ip).delete()
                print(result)
            except:
                return HttpResponse(0)
            return HttpResponse(1)

        return render(request, 'attendence/login.html', '')
