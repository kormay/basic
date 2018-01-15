
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# from django.shortcuts import render
from secu.models import Right
from django.conf.urls import url, include
from django.conf import urls
from django.conf import settings
from django.core.urlresolvers import RegexURLPattern, RegexURLResolver
from tools.ui.pager import get_record_index
from basic.render import render

class _Right:
 
    @staticmethod     
    def index(request):
        _Right.init_list()
        return render(request, 'secu/right.html', {})     

    @staticmethod     
    def list(request):
        if request.method == 'GET':
            record = get_record_index(request)
            total_records = Right.objects.all().count()
            li = Right.objects.all()[record['start']:record['end']]

            data = [
                        {
                         "id": item.id,
                         "name": item.name, 
                         "detail": item.detail,
                         "view_name": item.view_name,
                         "pattern": item.pattern,
                         "selector": item.selector
                        } 
                        for item in li
                   ]

            context = {
                "totalrecords": total_records,
                "data": data
            }
            return JsonResponse(context, safe=False)

#-------------------------------------------------------------------
    @staticmethod     
    def init_list():
        root_url_conf = __import__(settings.ROOT_URLCONF)
        urlpatterns = root_url_conf.urls.urlpatterns
        for url in urlpatterns:
            if isinstance(url, RegexURLPattern):
                _Right.urlpattern_to_right(url)
            elif isinstance(url, RegexURLResolver):
                for item in url.url_patterns:
                    _Right.urlpattern_to_right(item, url.regex.pattern, url.app_name)
    
    @staticmethod
    def urlpattern_to_right(urlpattern, parrent_pattern='', app_name=''):
        fn = urlpattern.callback
        if hasattr(fn, 'need_valid'):
            item = Right()
            item.view_name =  fn.__module__ + '.' + fn.__name__
            item.detail = '' if fn.__doc__ == None else fn.__doc__
            item.name = app_name + ':'+ urlpattern.name if app_name else urlpattern.name
            item.pattern = parrent_pattern + urlpattern.regex.pattern.replace('^', '') if parrent_pattern else urlpattern.regex.pattern

            if Right.objects.filter(view_name=item.view_name).count() == 0:
                item.save()