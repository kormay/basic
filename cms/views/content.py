from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from datetime import datetime

from cms.models import Category,KeyWord,Content,ContentKeyWord

class _Content:
    @staticmethod
    def add(request):
        if request.method == 'POST':
            category_code = request.POST['category']
            keys = request.POST['keys'].split(',')
            title = request.POST['title']
            description = request.POST['content']
            if category_code:
                if not Category.objects.filter(title=category_code):
                    Category.objects.create(title=category_code,code=category_code)
            else:
                category_code = '默认'
            category = Category.objects.get(title=category_code)
            content = Content.objects.create(title=title,description=description,category=category)

            if len(keys) > 0:
                for key in keys:
                    if not KeyWord.objects.filter(word=key):
                        KeyWord.objects.create(word=key)
                    else:
                        pass
                    key_word = KeyWord.objects.get(word=key)
                    ContentKeyWord.objects.create(key_word=key_word,content=content)

        return HttpResponse("Save success.")

    @staticmethod
    def edit(request):
        if request.method == 'POST':
            category_code = request.POST['category']
            keys = request.POST['keys'].split(',')
            title = request.POST['title']
            description = request.POST['content']
            id = request.POST['id']
            if category_code:
                if not Category.objects.filter(title=category_code):
                    Category.objects.create(title=category_code,code=category_code)
            else:
                category_code = '默认'
            category = Category.objects.get(title=category_code)
            content = Content.objects.filter(id=int(id)).update(title=title,description=description,category=category)

            if len(keys) > 0:
                for key in keys:
                    if not KeyWord.objects.filter(word=key):
                        KeyWord.objects.create(word=key)
                    else:
                        pass
                    key_word = KeyWord.objects.get(word=key)
                    ContentKeyWord.objects.create(key_word=key_word,content=Content.objects.get(id=int(id)))

        return HttpResponse("Save success.")

    @staticmethod
    def get_content_list_by_filter(request,id):
        content = Content.objects.get(id=id)
        content.entry_date = datetime.strftime(content.entry_date,'%Y-%m-%d %H:%M')
        context = {
            "content":content,
        }
        return render(request, 'cms/blog_one.html',context)

    @staticmethod
    def get_content_list_by_category(request):
        category = request.GET.get('category','0')
        content = Content.objects.all()
        totalrecords = content.count()
        if category != '0':
            content = Content.objects.filter(category=Category.objects.get(code=category))
            totalrecords = content.count()
        data = [{
            "id":item.id,
            "title":item.title,
            "category":item.category.title,
            "entry_date":datetime.strftime(item.entry_date,'%Y-%m-%d %H:%M')
            }for item in content]
        context = {
            "totalrecords":totalrecords,
            "data":data
        }
        return JsonResponse(context)

    @staticmethod
    def delete(request):
        if request.method == 'POST':
            id = int(request.POST["id"])
            try:
                content = Content.objects.get(pk=id)
                content.delete()
                return HttpResponse("成功删除")
            except Content.DoesNotExist:
                return HttpResponse("这条数据不存在。")
