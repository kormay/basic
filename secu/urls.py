from django.conf.urls import url
from secu.views import _Right, _Common, _Role, _User

app_name = 'secu'

urlpatterns = [
    # ex: /attendence/
    url(r'^$', _Common.index, name='index'),    

    url(r'^right/$', _Right.index, name='right'),
    url(r'^right/list/$', _Right.list, name='right_list'),

    url(r'^role/$', _Role.index, name='role'),
    url(r'^role/list$', _Role.list, name='role_list'),
    url(r'^role/single$', _Role.single, name='role_single'),
    url(r'^role/add$', _Role.add, name='role_add'),
    url(r'^role/edit$', _Role.edit, name='role_edit'),
    url(r'^role/del$', _Role.delete, name='role_del'),

    url(r'^role/add_delete_right$', _Role.add_delete_right_to_role, name='role_add_delete_right'),
    url(r'^role/right_list/(?P<role_id>[-\w]+)$', _Role.get_right_list_by_role, name='role_right_list'),

    url(r'^user/$', _User.index, name='user'),
    url(r'^user/add$', _User.add, name='user_add'),
    url(r'^user/del$', _User.delete, name='user_delete'),
    url(r'^user/edit$', _User.edit, name='user_edit'),
    url(r'^user/list$', _User.list, name='user_list'),
    url(r'^user/role_list/(?P<user_id>[-\w]+)$', _User.get_role_list_by_user, name='user_role_list'),
    url(r'^user/add_delete_role$', _User.add_delete_role_to_user, name='role_add_delete_role'),
]
