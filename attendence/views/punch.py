# from django.shortcuts import render
from basic.render import render
from django.core import serializers
from django.http import HttpResponse, JsonResponse
from datetime import datetime, timedelta
import time


from attendence.models import Punch
from attendence.decrator import *
from secu.models import User

class _Punch:
    @staticmethod
    @valid_user
    def index(request):
        user = User.objects.all()
        total_Records = User.objects.count()
        user_list = [{"user_name":u.user_name,"full_name":u.first_name + ' ' + u.last_name} for u in user]
        context = {
            "totalRecords": total_Records,
            "userlist": user_list
        }
        return render(request, 'attendence/punch_manage.html', context)

    @staticmethod
    @valid_user
    def add(request):
        if request.method == 'POST':
            punch_time = request.POST['punch_time']
            user_name = request.POST['user_name']
            user = User.objects.get(user_name=user_name)
            Punch.objects.create(user=user, punch_date=punch_time, is_normal=False, IP=request.get_host())
            return HttpResponse("Add punch info success.")

    @staticmethod         
    @valid_user
    def edit(request):
        if request.method == 'POST':
            punch_time = request.POST['punch_time']
            id = int(request.POST.get('id','0'))
            try:
                punch = Punch.objects.filter(id=id)
                if punch[0].is_normal == 1:
                    return HttpResponse("You can't edit this record.")
                else:
                    punch.update(punch_date=punch_time)
                    return HttpResponse("Edit punch info success.")
            except IndexError:
                return HttpResponse('This record does not exist.')

    @staticmethod
    @valid_user
    def delete(request):
        if request.method == 'POST':
            id = int(request.POST.get('id','0'))
            try:
                punch = Punch.objects.get(id=id)
                if punch.is_normal == 1:
                    return HttpResponse("You can't delete this record.")
                else:
                    punch.delete()
                    return HttpResponse("Delete success.")
            except Punch.DoesNotExist:
                return HttpResponse('This record does not exist.')
            
    @staticmethod
    @valid_user
    def get_list_by_filter(request):
        page_size = int(request.GET.get('pagesize', '10'))
        start_index = (int(request.GET.get('currentpage', '1')) - 1) * page_size+1
        start_index = 1 if start_index < 1 else start_index
        end_index = int(request.GET.get('currentpage', '1'))*page_size
        total_records,count,test = 0,0,0

        user_name_search = request.GET.get('user_name_search','0')
        start_search_punch_time = datetime.strptime(request.GET.get('punchtime_search_start','2016-01-01'),'%Y-%m-%d')
        start_search_punch_time_temp = start_search_punch_time
        end_search_punch_time = datetime.strptime(request.GET.get('punchtime_search_stop','2016-01-01'),'%Y-%m-%d')
        punch_list = []
        user = User.objects.all()
        if user_name_search == '0':
            total_records = (end_search_punch_time - start_search_punch_time + timedelta(days=1)).days*User.objects.all().count()
        else:
            user = User.objects.filter(user_name=user_name_search)
            total_records = (end_search_punch_time - start_search_punch_time + timedelta(days=1)).days       
        for i,e in enumerate(user):
            start_search_punch_time = start_search_punch_time_temp
            while start_search_punch_time <= end_search_punch_time:
                count += 1
                if start_index <= count <= end_index:
                    test += 1
                    list_somebody = e.punch_set.filter(punch_date__lt=start_search_punch_time+timedelta(days=1),
                        punch_date__gte=start_search_punch_time).order_by('punch_date')
                    if list_somebody.count() > 0:
                        punch_time_start = list_somebody[0].punch_date
                        punch_time_end = list_somebody[len(list_somebody)-1].punch_date
                        if (punch_time_start.hour < 9 or (punch_time_start.hour == 9 and punch_time_start.minute <= 10)) and punch_time_end.hour >= 18:
                            is_late = 'Normal'
                            color = 'black'
                        else:
                            is_late = 'Not Normal'
                            color = 'red'
                        punch_list.append({
                            "index":start_index+i+1,
                            "rownum": i+1,
                            "punch_date": datetime.strftime(start_search_punch_time,'%Y-%m-%d'),
                            "entry_date_start": datetime.strftime(punch_time_start,'%Y-%m-%d %H:%M:%S'), 
                            "entry_date_end": datetime.strftime(punch_time_end,'%Y-%m-%d %H:%M:%S'),
                            # "full_name": list_somebody[0].user.last_name + list_somebody[0].user.first_name,
                            "full_name": list_somebody[0].user.full_name,
                            "Status": is_late,
                            "color":color
                        })
                    else:
                        punch_list.append({
                            "index":start_index+i+1,
                            'rownum': i+1,
                            'punch_date': datetime.strftime(start_search_punch_time,'%Y-%m-%d'),
                            'entry_date_start': 'N/A', 
                            'entry_date_end': 'N/A',
                            # 'full_name': e.last_name + e.first_name,
                            'full_name': e.full_name,
                            'Status': 'Not Normal',
                            "color":"red"
                        })
                start_search_punch_time += timedelta(days=1)
        context = {
            "totalrecords": total_records,
            "data": punch_list,
        }
        return JsonResponse(context)

    @staticmethod
    @valid_user
    def get_all_list_by_filter(request):
        page_size = int(request.GET.get('pagesize', '10'))
        start_index = (int(request.GET.get('currentpage', '1')) - 1) * page_size
        start_index = 0 if start_index < 0 else start_index
        end_index = int(request.GET.get('currentpage', '1'))*page_size

        user_name_search_all = request.GET.get('user_name_searchall','0')
        punch_date_search_all = datetime.strptime(request.GET.get('punchdate_searchall','1900-01-01'),'%Y-%m-%d')
        user=User.objects.get(user_name=user_name_search_all)
        list_somebody = user.punch_set.filter(punch_date__gte=punch_date_search_all,
            punch_date__lt=punch_date_search_all + timedelta(days=1)).order_by('is_normal')
        punch_list = []
        for item in list_somebody:
            punch_list.append({
                "punch_id":item.id,
                "is_normal": "Yes" if item.is_normal else "No",
                "user_name":user_name_search_all,
                # "full_name":user.last_name + user.first_name,
                "full_name":user.full_name,
                "punch_time":datetime.strftime(item.punch_date,'%Y-%m-%d %H:%M:%S'),
                "punch_date":datetime.strftime(item.punch_date,'%Y-%m-%d')
            })
        return JsonResponse({"data":punch_list[start_index:end_index],"totalrecords":len(list_somebody)})
