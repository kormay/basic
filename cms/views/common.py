from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from datetime import datetime

from cms.models import Category,KeyWord,Content,ContentKeyWord

class _Common:
    @staticmethod
    def index(request):
        content_list = Content.objects.order_by('-entry_date')[:10]
        for item in content_list:
            item.description_part_two = item.description[670:]
            item.description_part_one = item.description[:670]
            item.entry_date = datetime.strftime(item.entry_date,'%Y-%m-%d %H:%M')
        context = {
            "content_list": content_list,
        }
        return render(request, 'cms/index.html', context)

    @staticmethod
    def get_category_key_list(request):
        id = int(request.GET.get('id','0'))
        if id == 0:
            category = Category.objects.exclude(title='').exclude(title='请选择分类...')
            key_word = KeyWord.objects.exclude(word='')
            context = {
                "category":category,
                "key_word":key_word,
            }
        else:
            content = Content.objects.get(id=id)
            contentkeyword_list = content.contentkeyword_set.filter(content=content)
            word = ''
            for i,item in enumerate(contentkeyword_list):
                if i == 0:
                    word = item.key_word.word
                else:
                    word = word + ',' + item.key_word.word
            key_word = KeyWord.objects.all()
            category = Category.objects.all()
            context = {
                "id":id,
                "content":content,
                "word":word,
                "key_word":key_word,
                "category":category
            }
        return render(request, "cms/add.html",context)