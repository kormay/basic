# BSQJ
BootStrap table paging

#只需要很少的代码就能实现自动填充和分页
![](https://github.com/wancy86/BSQJ/blob/master/pager.png)

#初始化表格和分页
```javascript
    $("#iplisttable").pagingTable({
        json_url: "{% url 'attendence:ip_json'%}",
        pageSize: 2,
        pageNumber: 10, /*default 10*/
        separator: "#" /*default #*/,
        callback: function(){console.log('this is callback...');}
    });
```
<hr>
#version 2.1 changes:
1. 支持模板语法，指定分隔符，默认为 #

2. 调整html结构，更符合一般的table结构

3. 支持回调，在加载数据之后可以添加逻辑

4. 支持自定义显示页码的个数，默认10个

#html结构范例:
```html
    <table id="iplisttable" class="table table-bordered table-hover table-striped">
        <thead>
            <tr>
                <th width="20%">Name</th>
                <th width="20%">IP</th>
                <th width="20%">Action</th>
            </tr>
        </thead>
        <tbody>
            <tr pk="#ip#" template=1 style="display: none">
                <td>#name#</td>
                <td>#ip#</td>
                <td>
                    <a href="javascript:void(0)" onclick="delIP(this)" class="delip" style="cursor:pointer">
                        <span class="glyphicon glyphicon-floppy-remove"></span> <span>(#ip#)</span>
                    </a>
                    <a style="cursor:pointer;display:inline-block;margin-left:15px;">
                        <span class="glyphicon glyphicon-edit"></span>
                    </a>
                </td>
            </tr>
        </tbody>
    </table>
```

#后台数据接口
```python
def ip_json(request):

    pagesize = int(request.GET.get('pagesize', 10))
    startindex = (int(request.GET.get('currentpage', 1)) - 1) * pagesize
    startindex = 0 if startindex < 0 else startindex
    endindex = startindex + pagesize

    totalRecords = EmployeeIP.objects.all().select_related().count()
    employeeips = EmployeeIP.objects.all().select_related()[startindex:endindex]
    data = [{"rownum": index + 1, "name": eip.employee.first_name + ' ' + eip.employee.last_name, "ip": eip.IP} for index, eip in enumerate(employeeips)]

    json_result = {
        "totalrecords": totalRecords,
        "data": data
    }
    return JsonResponse(json_result, safe=False)
```



