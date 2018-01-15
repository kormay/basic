from cms.views.common import _Common
from cms.tests.test_base import TestBase
from cms.models import Content
from cms.models import Category

class Index(TestBase):
    @classmethod
    def setUpTestData(cls):
        for i in range(5):
            category = Category()
            category.title = 'raymon' + str(i)
            category.code = 'raymon' + str(i)
            category.save()
            content = Content()
            content.title = 'raymon test'
            content.description = str(i) + '与此同时，一项民意调查显示英国留欧阵营领先3个百分点，提升了投资者的风险偏好。高盛上月曾警告称，人民币走软可能引发资本外流，加强对人民币一次性贬值的押注。日内人民币兑美元上涨0.11%至6.5795附近，上周早些时候一度跌至5年低点后连续第2个交易日走高。与此同时，离岸人民币上涨0.2%。此外，欧元和英镑兑美元也上涨超过0.7%。'
            content.category = category
            content.save()

    def test_index(self):
        request = self.request
        request.method = 'GET'
        response = _Common.index(request)
        self.assertContains(response,"1与此同时，一项民")
        self.assertContains(response,"3与此同时，一项民")
        self.assertEqual(response.status_code, 200)