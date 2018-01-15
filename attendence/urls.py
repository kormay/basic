from django.conf.urls import url
from attendence.views import employee, _Punch, IP, account, leave

app_name = 'attendence'

urlpatterns = [
    # ex: /attendence/
    url(r'^index$', account.index, name='index'),
    url(r'^change/password$', account.change_password, name='change_password'),
    url(r'^change/password/check_old_password$', account.check_old_password, name='check_old_password'),

    # ex: ^attendence/punch/manage
    url(r'^punch$', _Punch.index, name='punch_index'),
    url(r'^punch/add/', _Punch.add, name="punch_add"),
    url(r'^punch/edit/', _Punch.edit, name="punch_edit"),
    url(r'^punch/delete/', _Punch.delete, name="punch_delete"),
    # url(^'^punch/get_names/', punch.get_names, name="get_names"),
    url(r'^punch/get_list_by_filter/', _Punch.get_list_by_filter, name="get_list_by_filter"),
    url(r'^punch/get_all_list_by_filter/', _Punch.get_all_list_by_filter, name="get_all_list_by_filter"),
    # url(^'^punch/punchoinfo_search/(?P<search1>\S+)/(?P<search2>\S+)/(?P<username>\S+)/$', punch.punchoinfo_search, name="punchoinfo_search"),
    # url(^'^punch/getsomeone_Allpunchinfo/(?P<username_searchAll>\S+)/(?P<punchdate_searchAll>\S+)/$', punch.getsomeone_Allpunchinfo, name="getsomeone_Allpunchinfo"),
    # url(^'^punch/Edit_savepunchinfo/(?P<username_searchAll>\S+)/(?P<punchdate_searchAll>\S+)/(?P<id>\S+)/(?P<punch_time>\S\S\S\S\S\S\S\S\S\S\s\S+)/$', punch.Edit_savepunchinfo, name="Edit_savepunchinfo"),

    # ex: ^/attendence/employee/manage

    # url(r'^employee/manage$', employee.index, name='employee_index'),
    # url(r'^employee/manage/get_list$', employee.get_list, name='get_list'),
    # url(r'^employee/manage/add$', employee.add, name='employee_add'),
    # url(r'^employee/manage/delete$', employee.delete, name='employee_delete'),
    # url(r'^employee/manage/edit$', employee.edit, name='employee_edit'),


    # url ^ction name
    url(r'^ip$', IP.index, name='ip_manage'),
    url(r'^ip/get_list$', IP.get_list, name='ip_get_list'),
    url(r'^ip/add$', IP.add, name='ip_add'),
    url(r'^ip/del$', IP.delete, name='ip_delete'),

    url(r'^leave$', leave.index, name='leave_manage'),
    url(r'^leave/add$', leave.add, name='leave_add'),
    url(r'^leave/json$', leave.get_list, name='leave_get_list'),
    url(r'^leave/approve_deny$', leave.approve_deny, name='leave_approve_deny'),

    #test validator 
    url(r'^validator$', employee.index, name='validator_index'),
]
