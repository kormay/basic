
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from attendence.urls import urlpatterns

from django.conf.urls import url, include

# __init__(self, regex, callback, default_args=None, name=None)

class _Common:
    @staticmethod
    def index(request):
         return render(request, 'secu/index.html')

# def get_init_list(request):

#     url = urlpatterns[0]

#     Right.objects.create(
#         name = url.name,
#         detail = url.name,
#         view_name = url.callback.__module__ + '.' +url.callback.__name__,
#         pattern = url.regex.pattern
#     )

#     return HttpResponse("Hello World")