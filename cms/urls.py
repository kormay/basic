from django.conf.urls import url

from cms.views import _Common,_Content,_Category

app_name = 'cms'

urlpatterns = [
    url(r'^$', _Common.index, name='index'),
    url(r'^add/$', _Content.add, name='add'),
    url(r'^edit/$', _Content.edit, name='edit'),
    url(r'^get_category_key_list/$', _Common.get_category_key_list, name='get_category_key_list'),
    url(r'^get_content_list_by_filter/(?P<id>\d+)/$', _Content.get_content_list_by_filter, name='get_content_list_by_filter'),
    url(r'^get_list/$', _Category.get_list, name='get_category_list'),
    url(r'^get_list/get_content_list_by_category/$', _Content.get_content_list_by_category, name='get_content_list_by_category'),
    url(r'^get_list/add_category/$', _Category.add, name='add_category'),
    url(r'^delete/$', _Content.delete, name='content_delete'),
]
