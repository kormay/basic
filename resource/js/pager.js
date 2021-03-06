/*
 *Name: BootStrap Pager 
 *Author: CooMark
 *version: 2.1.3
 *BootStrap version: 3.0
 */
(function($) {
    $.fn.pagingTable = function(options) {
        var table = $(this);
        var settings = $.extend({
            json_url: null,
            pageSize: 10,
            pageNumber: 10,
            separator: "#",
            callback: null
        }, options);

        if (!table.is("table")) {
            return this;
        }

        table.data({
            pagesize: settings.pageSize,
            currentpage: 1,
            dataurl: settings.json_url,
            totalrecords: 0,
            callback: settings.callback,
            pageNumber: settings.pageNumber,
            pagebar: 'pagerbar_' + table.attr("id")
        });

        var load_json = function(currentpage) {
            var currentpage = currentpage || 1;
            Class.ajax({
                url: settings.json_url,
                method: 'get',
                data: 'pagesize=' + settings.pageSize + '&currentpage=' + currentpage,
                success: function(resp) {
                        var data = resp.data;
                        if (!data) {
                            return;
                        }
                        var re_pagebar = table.data('totalrecords') == resp.totalrecords ? 0 : 1;
                        table.data('totalrecords', resp.totalrecords);
                        table.data('totalpages', Math.ceil(resp.totalrecords / settings.pageSize));
                        table.find('tbody tr[template!=1]').remove();

                        //re-generate the paging bar
                        var template = table.find("tbody tr[template=1]");
                        var tds = template.find('td');

                        var datarow = (template.clone())
                            .removeAttr('template')
                            .removeAttr('style');

                        var template_str = $("<div></div>").append(datarow).html();

                        for (var dr = 0; dr < data.length; dr++) {
                            var newrow = template_str;
                            for (var field in data[dr]) {
                                var reg = new RegExp(settings.separator + field + settings.separator, 'ig');
                                newrow = newrow.replace(reg, data[dr][field]);
                            }
                            table.find('tbody').append(newrow);
                        }

                        //keep pagebar position fixed
                        if (data.length < table.data('pagesize')) {
                            var i = parseInt(table.data('pagesize')) - data.length;
                            for (; i > 0; i--) {
                                var newrow = $(template_str).clone().css('visibility', 'hidden');
                                table.find('tbody').append(newrow);
                            }
                        }

                        if (re_pagebar) {
                            getPageBar(1);
                        }

                        if (settings.callback && typeof(settings.callback) == 'function') {
                            settings.callback();
                        }

                        $("#" + table.data('pagebar')).find('li.total span').text(currentpage + ' / ' + table.data('totalpages'));

                    } //end success
            });
        };

        load_json(1);

        var getPageBar = function(startPage, activePage) {
            var totalpages = table.data('totalpages');
            if (totalpages == 1) {
                return;
            }
            var activePage = activePage || (startPage || 1);
            var startPage = startPage || 1;
            var endPage = startPage + settings.pageNumber - 1;
            endPage = endPage > totalpages ? totalpages : endPage;

            var tmp = '';
            tmp += "<nav>";
            tmp += "    <ul class='pagination'>";
            if (totalpages > table.data('pageNumber')) {
                tmp += "        <li title='First Page' class='disabled first'><a href='javascript:void(0)' aria-label='First'><span class='glyphicon glyphicon-step-backward'></span></a></li>";
                tmp += "        <li title='Previous " + table.data('pageNumber') + " Pages' class='disabled previous'><a href='javascript:void(0)' aria-label='Next'><span class='glyphicon glyphicon-chevron-left'></span></a></li>";
            }
            var header = tmp;
            var pagers = "";

            for (i = startPage; i <= endPage; i++) {
                pagers = pagers + "<li><a href='javascript:void(0)'>" + i + "</a></li>";
            }

            tmp = ''
            if (totalpages > table.data('pageNumber')) {
                tmp += "        <li title='Next " + table.data('pageNumber') + " Pages' class='next'><a href='javascript:void(0)' aria-label='Previous'><span class='glyphicon glyphicon-chevron-right'></span></a></li>";
                tmp += "        <li title='Last Page' class='last'><a href='javascript:void(0)' aria-label='First'><span class='glyphicon glyphicon-step-forward'></span></a></li>";
                tmp += "        <li class='total'><span></span></li>";
            }

            tmp += "    </ul>";
            tmp += "</nav>";
            var footer = tmp;

            $("#" + table.data('pagebar')).remove();
            var pagerbar = $("<div></div>").attr("id", table.data('pagebar'));
            pagerbar.html(header + pagers + footer).insertAfter(table);

            pagerbar.find('li').on("click", function() {
                page_click(this);
            });

            pagerbar.find('li').each(function() {
                if ($(this).find('a:eq(0)').text() == activePage) {
                    page_click(this);
                }
            });

        };

        var page_click = function(obj) {
            if ($(obj).hasClass('disabled')) {
                return false;
            }

            var pagerbar = $(obj).parents('ul');
            var totalpages = table.data('totalpages');
            var pageNumber = table.data('pageNumber');
            var startPage = parseInt(pagerbar.find("li:eq(2) a").text());
            var endPage = startPage + pageNumber - 1;
            endPage = endPage > totalpages ? totalpages : endPage;

            var currentpage = table.data('currentpage');
            var page_index = currentpage;

            if ($(obj).hasClass('previous')) {
                getPageBar(startPage - pageNumber);
                return;
            } else if ($(obj).hasClass('next')) {
                getPageBar(startPage + pageNumber);
                return;
            } else if ($(obj).hasClass('first')) {
                getPageBar(1);
                return;
            } else if ($(obj).hasClass('last')) {
                getPageBar(totalpages - table.data('pageNumber') + 1, totalpages);
                return;
            } else {
                page_index = $(obj).find('a').text();
            }

            pagerbar.find('li').removeClass('disabled').removeClass('active');

            if (startPage <= 1 || totalpages <= pageNumber) {
                pagerbar.find('li.previous, li.first').addClass('disabled');
            }
            if (endPage >= totalpages || totalpages <= pageNumber) {
                pagerbar.find('li.next, li.last').addClass('disabled');
            }

            page_index = parseInt(page_index);
            table.data('currentpage', page_index);
            pagerbar.find('li').each(function() {
                if ($(this).find('a:eq(0)').text() == page_index) {
                    $(this).addClass('active');
                }
            });

            if (page_index != currentpage) {
                load_json(page_index);
            }
        };

        return this;
    };

})($);
