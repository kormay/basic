from django.conf.urls import url
from todolist.views import _Item, _Step, _Status, _ItemWork

app_name = 'todolist'

urlpatterns = [
    url(r'^item/$', _Item.index, name='item'),
    url(r'^item/list$', _Item.list, name='item_list'),
    url(r'^item/instance$', _Item.instance, name='item_instance'),
    url(r'^item/add$', _Item.add, name='item_add'),
    url(r'^item/edit$', _Item.edit, name='item_edit'),
    url(r'^item/del$', _Item.delete, name='item_delete'),
    url(r'^item/workflow$', _Item.workflow, name='item_workflow'),

    url(r'^item-workflow/add$', _ItemWork.add, name='item-workflow_add'),
    url(r'^item-workflow/delete$', _ItemWork.delete, name='item-workflow_delete'),
    url(r'^item-workflow/edit$', _ItemWork.edit, name='item-workflow_edit'),
    url(r'^item-workflow/list$', _ItemWork.list, name='item-workflow_list'),
    url(r'^item-workflow/instance$', _ItemWork.instance, name='item_work_instance'),

    url(r'^step/$', _Step.index, name='step'),
    url(r'^step/list$', _Step.list, name='step_list'),
    url(r'^step/add$', _Step.add, name='step_add'),
    url(r'^step/edit$', _Step.edit, name='step_edit'),
    url(r'^step/del$', _Step.delete, name='step_delete'),

    url(r'^status/$', _Status.index, name='status'),
    url(r'^status/list$', _Status.list, name='status_list'),
    url(r'^status/add$', _Status.add, name='status_add'),
    url(r'^status/edit$', _Status.edit, name='status_edit'),
    url(r'^status/del$', _Status.delete, name='status_delete'),
]
