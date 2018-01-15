from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from datetime import datetime
import time

from cms.models import Category,KeyWord,Content,ContentKeyWord

class _Category:
    @staticmethod
    def add(request):
        if request.method == "POST":
            category = request.POST["category"]
            category_list = Category.objects.filter(title=category)
            if len(category_list) > 0:
                return HttpResponse('类别"'+ category +'"已经存在。')
            else:
                # time.sleep(10)
                Category.objects.create(title=category,code=category)
                return HttpResponse("成功添加。")

    @staticmethod
    def get_list(request):
        if request.method == "GET":
            category = Category.objects.exclude(title='').exclude(title='请选择分类...').exclude(title='0')
            context = {
                "category":category
            }
            return render(request, 'cms/manage.html', context)