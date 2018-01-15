function CheckKey() {
    if (window.event.ctrlKey) {
        return 1;
    } else if (window.event.altKey) {
        return 2;
    } else if (window.event.button == 2) {
        return 3;
    } else {
        return 0;
    }
}

function LimitRightMenu() {
    if (window.Event)
        document.captureEvents(Event.MOUSEUP);

    function nocontextmenu() {
        event.cancelBubble = true
        event.returnvalue = false;
        return false;
    }

    function norightclick(e) {
        if (window.Event) {
            if (e.which == 2 || e.which == 3)
                return false;
        } else if (event.button == 2 || event.button == 3) {
            event.cancelBubble = true
            event.returnvalue = false;
            return false;
        }
    }
    document.oncontextmenu = nocontextmenu; // for IE5+ 
    document.onmousedown = norightclick; //
}

function Line(x0, y0, x1, y1, color) {
    var rs = "";

    var lx = x1 - x0;
    var ly = y1 - y0;
    var line = Math.sqrt(lx * lx + ly * ly);
    rs = new Array();
    var px = 0,
        py = 0;
    var i = 0;
    var pointLen = 6;
    var crossLine = 10;

    rs.push("<a class='dragLine'>");
    //画线
    for (; i < line - pointLen; i += 2) {
        var p = i / line;
        px = parseInt(x0 + lx * p);
        py = parseInt(y0 + ly * p);
        rs.push("<div  style='top:" + py + "px;left:" + px + "px;height:2px;width:2px;position:absolute;font-size:1px;background-color:" + color + "'></div>");
    }

    //画箭头
    for (var j = line - pointLen - 3; j < line; j += 1) {
        var p = j / line;
        px = parseInt(x0 + lx * p);
        py = parseInt(y0 + ly * p);
        rs.push("<div  style='top:" + py + "px;left:" + px + "px;height:1px;width:1px;position:absolute;font-size:1px;background-color:" + color + "'></div>");
        crossLine -= 1
        for (var y = 0; y < crossLine; y += 1) {
            px = parseInt(x0 + lx * p + (y - crossLine / 2) * ly / line);
            py = parseInt(y0 + ly * p - (y - crossLine / 2) * lx / line);
            rs.push("<div style='top:" + py + "px;left:" + px + "px;height:1px;width:1px;position:absolute;font-size:1px;background-color:" + color + "'></div>");
        }
    }
    rs.push("</a>");
    rs = rs.join("");
    return rs;
}

var DrawLine = function(route) {
    this.beginTarget = $("div[fn-type=drag][order='" + route.split('_')[0] + "']");
    this.endTarget = $("div[fn-type=drag][order='" + route.split('_')[1] + "']");
    this.route = route;
    DrawLine.prototype.draw = function() {
        if (this.route.split('_')[0] == this.route.split('_')[1]) return;
        x0 = this.beginTarget.width() / 2;
        y0 = this.beginTarget.height();
        x1 = this.endTarget.offset().left + this.endTarget.width() / 2 - this.beginTarget.offset().left;
        y1 = this.endTarget.offset().top - this.beginTarget.offset().top;

        this.beginTarget.find("a[route='" + this.route + "']").remove();
        this.beginTarget.append(Line(x0, y0, x1, y1, '#ddd'));
        this.beginTarget.find("a:not([route])").attr("route", this.route);
    }
}

//如果是页面初始化，这type=true,则会重绘所有连接线，
//如果是拖拽type不传或为false，则会重绘所有拖动影响的线
function RedrawLine(type) {
    var kind = '.active';
    var lines = [];
    if (type == true) {
        kind = '';
    }
    $('div[fn-type=drag]' + kind).each(function() {
        var order = $(this).attr('order');
        $("a[route^='" + order + "_'],a[route$='_" + order + "']").each(function() {
            lines.push(new DrawLine($(this).attr("route")));
        });
    });
    $.each(lines.drawLineUnique(), function() {
        this.draw();
    });
}

function StepAdapter() {
    this.max_order = 0;
    this.step_template = {
        step_start: {
            name: "Start",
            order: 1,
            coordinate_x: 420,
            coordinate_y: 50,
            author: [{ name: "", value: "", category: "" }]
        },
        step_new: {
            name: "New",
            order: 2,
            coordinate_x: 420,
            coordinate_y: 750,
            author: [{ name: "", value: "", category: "" }]
        },
        step_end: {
            name: "End",
            order: 99,
            coordinate_x: 420,
            coordinate_y: 250,
            author: [{ name: "", value: "", category: "" }]
        }
    };
    this.template_obj = $('div[fn-type=drag]:hidden[template=True]');

    StepAdapter.prototype.CreateStep = function(json, left, top) {
        var obj = this.template_obj.clone();
        obj.removeClass('hidden').removeAttr('template');
        $('#chart').append(obj);
        obj.draggable({
            containment: 'parent',
            cursor: 'move',
            cursorAt: {
                top: 50,
                left: 60
            },
            scroll: true,
            start: function(event, ui) {
                orign_top = ui.position.top;
                orign_left = ui.position.left;
                $('div[fn-type=drag].active').not(this).each(function() {
                    $(this).data('offset', $(this).offset());
                });
            },
            drag: function(event, ui) {
                goal_top = ui.position.top;
                goal_left = ui.position.left;
                //拖动所有被选中的drag[]
                if ($(this).hasClass('active')) {
                    $('div[fn-type=drag].active').not(this).each(function() {
                        var orign_coordinate = $(this).data('offset');
                        $(this).offset({
                            left: orign_coordinate.left + goal_left - orign_left,
                            top: orign_coordinate.top + goal_top - orign_top
                        });
                    });
                }
                //重绘所有相关线条
                RedrawLine();
            }
        }).on('click', function() {
            if (CheckKey() == 1) {
                if ($(this).hasClass('active')) {
                    $(this).removeClass('active');
                } else {
                    $(this).addClass('active');
                }
            } else if (CheckKey() == 2) {
                var orign_drap = $('div[fn-type=drag].active');
                if (orign_drap && orign_drap.length == 1) {
                    new DrawLine(orign_drap.attr('order') + '_' + $(this).attr('order')).draw();
                }
            } else {
                $(this).addClass('active');
                $('div[fn-type=drag].active').not(this).removeClass('active');
            }
        }).on('dblclick', function() {
            $('#step_info').modal('show');
        });
        if (json) {
            var data_source = {}
            $.each(this.step_template.step_new, function(key, value) {
                if (key instanceof Array) {
                    var arr = [];
                    $.each(value, function(key, child) {
                        var obj = {};
                        $.each(child, function(key, item) {
                            obj[key] = item;
                        });
                        arr.push(obj);
                    });
                    data_source[key] = arr;
                } else {
                    data_source[key] = json[key];
                }
            });
            obj.find('div[name=head]').html(json.name);
            obj.attr('order', json.order);
            obj.data('data_source', data_source);
            obj.css('left', json.coordinate_x);
            obj.css('top', json.coordinate_y);
        } else {
            if (this.max_order == 98) {
                this.max_order += 2;
            } else {
                this.max_order += 1;
            }
            obj.find('div[name=head]').html('New Step');
            obj.attr('order', this.max_order);
            obj.offset({
                left: left,
                top: top
            });
        }
    };
    StepAdapter.prototype.InitializeStep = function(json) {
        var step_adapter = this;
        if (json) {
            var json_obj = JSON.parse(json);
            var temp_order = 0;
            $.each(json_obj.steps, function(key, value) {
                if (value.order > temp_order && value.order != 99) {
                    temp_order = value.order;
                }
                step_adapter.CreateStep(value);
            });
            step_adapter.max_order = temp_order;
        } else {
            $.each(this.step_template, function(key, value) {
                if (key != 'step_new') {
                    step_adapter.CreateStep(value);
                }
            });
            step_adapter.max_order = 1;
        }
    };
    StepAdapter.prototype.Param = function(obj) {
        if (obj) {
            $.each(obj, function(key, value) {
                if (value instanceof Array) {
                    $('#step_info').find('[name=' + key + ']').data('ms_' + key, value);
                    if (value) {
                        var display_value = [];
                        $.each(value, function(key, child) {
                            display_value.push(child.name);
                        });
                        $('#step_info').find('[name=' + key + ']').val(display_value.join(';'));
                    }
                } else {
                    $('#step_info').find('[name=' + key + ']').Val(value);
                }
            });
        } else {
            var param_obj = {}
            $.each(this.step_template.step_new, function(key, value) {
                if (value instanceof Array) {
                    var arr = [];
                    var goal_obj = $('#step_info').find('[name=' + key + ']').data('ms_' + key);
                    if (goal_obj) {
                        $.each(goal_obj, function(key, child) {
                            var obj = {};
                            $.each(value, function(key, item) {
                                obj[key] = child[key];
                            });
                            arr.push(obj);
                        });
                    }
                    param_obj[key] = arr;
                } else {
                    var goal_obj = $('#step_info').find('[name=' + key + ']');
                    param_obj[key] = goal_obj.val();
                }
            });
            return param_obj;
        }
    };
    StepAdapter.prototype.Clear = function() {
        var targetObj = $('#step_info');
        $("textarea,:text,:password,input[type=email]", targetObj).each(function() {
            $(this).val("");
        });
        $("select", targetObj).each(function() {
            $(this).val("-1");
            $(this).change();
        });
        $(":radio,:checkbox", targetObj).each(function() {
            $(this).attr("checked", false);
            $(this).change();
        });
        $.each(targetObj.data(), function(key, value) {
            if (/^ms_.+$/.test(key)) {
                targetObj.removeData(key);
            }
        });
        $.each(this.step_template.step_new, function(key, value) {
            if (value instanceof Array) {
                var goal_obj = targetObj.find('[name=' + key + ']')
                $.each(goal_obj.data(), function(key, value) {
                    if (/^ms_.+$/.test(key)) {
                        goal_obj.removeData(key);
                    }
                });
            }
        });
    };
}


Array.prototype.drawLineUnique = function() {
    var arr = [];
    var tempobj = {};
    $.each(this, function() {
        var orign_arr = this;
        var flag = false;
        $.each(arr, function() {
            if (this.route == orign_arr.route) {
                flag = true;
            }
        });
        if (!flag) arr.push(orign_arr);
    });
    return arr;
}
