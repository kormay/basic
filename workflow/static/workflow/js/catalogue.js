 // var data = {
 //        catalogue: [{
 //            title: "Content",
 //            enable_add: true,
 //            add_desc:"新增流程",
 //            add_event:test1,
 //            items: [{
 //                id: "1",
 //                title: "asdf",
 //                desc: "随便",
 //                content: "定义流程",
 //                event: test,
 //            }, {
 //                id: "2",
 //                title: "asdf",
 //                desc: "随便",
 //                content: "定义流程",
 //                event: test,
 //            }, {
 //                title: "asdf",
 //                desc: "随便",
 //                content: "定义流程"
 //            }, {
 //                title: "asdf",
 //                desc: "随便",
 //                content: "定义流程"
 //            }]
 //        }, {
 //            title: "Content",
 //            items: [{
 //                title: "asdf",
 //                desc: "随便",
 //                content: "定义流程"
 //            }, {
 //                title: "asdf",
 //                desc: "随便",
 //                content: "定义流程"
 //            }, {
 //                title: "asdf",
 //                desc: "随便",
 //                content: "定义流程"
 //            }]
 //        }]
 //    };
(function() {
    function catalogue_fn(target, obj) {
        var catalogue_obj = this;
        var target_obj = target;
        var catalogue_data = obj;

        var catalogue_container = '<div class="catalogue"> <h3 class="catalogue-head-title"><span class="badge catalogue-head-total"></span></h3> <ul class="catalogue-inner container"> </ul> </div>'
        var catalogue_item = '<li class="catalogue-item col-lg-3 text-center"><a href="javascript:void(0)"><h4 class="catalogue-item-title"></h4><h6 class="catalogue-item-desc"></h6><span></span></a></li>';
        var catalogue_item_add = '<li class="catalogue-item-add col-lg-3 text-center"><a href="javascript:void(0)"><div></div><p>新增添加</p></a></li>'
        catalogue_fn.prototype.CreateItem = function(data) {
            var item = $(catalogue_item);

            item.find('ul').append(catalogue_item);
            if (data.title) item.find('h4').html(data.title);
            if (data.desc) item.find('h6').html(data.desc);
            if (data.content) item.find('span').html(data.content);
            if (data.event) item.find('a').on('click', { id: data.id }, data.event);

            return item;
        }

        catalogue_fn.prototype.Init = function() {
            if (catalogue_data.catalogue) {
                $.each(catalogue_data.catalogue, function(key, value) {
                    var container = $(catalogue_container);
                    if (value.title) container.find('h3').prepend(value.title);
                    if (value.items) {
                        container.find('span').html('' + value.items.length);
                        $.each(value.items, function(key, value) {
                            container.find('ul').append(catalogue_obj.CreateItem(value));
                        });
                    }
                    if (value.enable_add) {
                        var add_obj = $(catalogue_item_add);
                        if (value.add_desc) add_obj.find('p').html(value.add_desc);
                        if (value.add_event) add_obj.find('a').on('click', value.add_event);
                        container.find('ul').append(add_obj);
                    }
                    target_obj.append(container);
                });
            }
        }
    }

    $.fn.Catalogue = function(obj) {
        var catalogue = new catalogue_fn(this, obj);
        catalogue.Init();
        return this;
    }
})(jQuery);
