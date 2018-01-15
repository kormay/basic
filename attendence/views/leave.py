from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.core import serializers
from django.core.urlresolvers import reverse
from attendence.models import Adjustment, AdjustmentLog
from django.db.utils import IntegrityError
from attendence.decrator import valid_user
from secu.models import User
from tools import is_valid_date

@valid_user
def index(request):
    return render(request, 'attendence/leave_manage.html')

@valid_user
def get_list(request): 
    page_size = int(request.GET.get('pagesize', 10))
    start_index = (int(request.GET.get('currentpage', 1)) - 1) * page_size
    start_index = 0 if start_index < 0 else start_index
    end_index = start_index + page_size 
    total_records = Adjustment.objects.all().count()

    data = []
    index = 1
    for adj in Adjustment.objects.all()[start_index:end_index]:
        rec = {
                "rownum": index, 
                "id": adj.id, 
                "name": adj.user.first_name + ' ' + adj.user.last_name,
                "start_date": adj.start_datetime, 
                "end_date": adj.end_datetime
              }
        adj_log = AdjustmentLog.objects.filter(adjustment=adj)
        if adj_log.count() == 0:
            rec['status'] = 'Waiting' 
            rec['btn_class'] = 'show_inline'
        elif adj_log.last().operation == '1':
            rec['status'] = 'Approved'
            rec['btn_class'] = 'hide'
        else: 
            rec['status'] = 'Denied'
            rec['btn_class'] = 'hide'
        data.append(rec)
        
    json_result = {
        "totalrecords": total_records,
        "data": data
    }
    return JsonResponse(json_result, safe=False)

@valid_user
def add(request):
    if request.method == "POST":
        start_date = request.POST.get('StartDate')
        end_date = request.POST.get('EndDate')
        if is_valid_date.is_valid_date(start_date) and is_valid_date.is_valid_date(end_date): 
            Adjustment.objects.create(
                user=User.objects.get(user_name=request.session.get('user_name')),
                adjustment_type='L',
                start_datetime=start_date,
                end_datetime=end_date
            ) 
            return HttpResponse('Leave apply success')
        else:
            return HttpResponse('The date is not in the correct style.')

@valid_user
def approve_deny(request):
    if request.method == "POST":
        AdjustmentLog.objects.create(
            adjustment = Adjustment.objects.get(id = request.POST.get('id')),
            operation = request.POST.get('operation')            
        )
        return HttpResponse('The leave apply has been approved/denied.')


