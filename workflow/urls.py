from django.conf.urls import url
from workflow.views.start_process import _StartProcess
from workflow.views.define_process import _DefineProcess
from workflow.views.category_process import _CategoryProcess
app_name = 'workflow'

urlpatterns = [
    url(r'^$', _StartProcess.index, name='index'),

    url(r'^process/$', _StartProcess.index, name='start_process_index'),
    url(r'^define/$', _DefineProcess.index, name='define_process_index'),
    url(r'^define/save/$', _DefineProcess.save, name='define_process_save'),
    url(r'^category/$', _CategoryProcess.index, name='category_process_index'),
]
