from collections import namedtuple

'''this method would return a dictionary, include start and end'''
def get_record_index(request):
    page_size = int(request.GET.get('pagesize') if request.GET.get('pagesize') else 10)
    page_index = int(request.GET.get('currentpage') if request.GET.get('currentpage') else 1)

    start = (page_index - 1) * page_size
    end = start + page_size 

    result = {'start': start, 'end': end}
    return result   
