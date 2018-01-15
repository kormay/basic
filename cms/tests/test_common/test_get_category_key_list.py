from cms.tests.test_base import TestBase
from cms.models import Category,KeyWord,Content,ContentKeyWord
from cms.views.common import _Common

class GetCategortKeyList(TestBase):
    @classmethod
    def setUpTestData(cls):
        keyword_common = KeyWord()
        keyword_common.word = 'key1000'
        keyword_common.save()
        for i in range(5):
            category = Category()
            category.title = 'raymon' + str(i)
            category.code = 'raymon' + str(i)
            category.save()
            keyword = KeyWord()
            keyword.word = 'key' + str(i)
            keyword.save()
            content = Content()
            content.title = 'raymon test' + str(i)
            content.description = '大煞笔' + str(i)
            content.category = category
            content.save()
            contentkeyword = ContentKeyWord()
            contentkeyword.content = content
            contentkeyword.key_word = keyword
            contentkeyword.save()
            contentkeyword = ContentKeyWord()
            contentkeyword.content = content
            contentkeyword.key_word = keyword_common
            contentkeyword.save()

            
    def setUp(self):
        self.pk = Content.objects.get(title='raymon test2').id
        super().setUp()

    def test_get_category_key_list_id_is_0(self):
        request = self.request
        request.method = 'GET'
        request.GET['id'] = '0'
        response = _Common.get_category_key_list(request)
        self.assertContains(response, '<input id="keys" type="text" class="form-control" value=""')
        self.assertContains(response, '<option value="0">请选择分类...</option>')

    def test_get_category_key_list_id_not_0(self):
        request = self.request
        request.method = 'GET'
        request.GET['id'] = str(self.pk)
        response = _Common.get_category_key_list(request)
        self.assertContains(response, 'raymon test2')
        self.assertContains(response, '大煞笔2')
        self.assertContains(response, 'raymon')
        self.assertContains(response, 'key2,key1000')