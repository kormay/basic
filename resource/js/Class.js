Base = function() {
    var _Base = function() {
        this.init.apply(this, arguments);
    }

    _Base.fn = _Base.prototype;
    _Base.fn.init = function() {};

    _Base.proxy = function(func) {
        var self = this;
        return (function() {
            return func.apply(self, arguments);
        });
    }

    return _Base;
}

var Class = new Base();

Class.ajax = function(obj) {
    Class.showProgress();

    var success = obj.success;
    obj.success = function(response, textStatus, xhr) {
        if (xhr.getResponseHeader('redirect')) {
            alert("会话已经过期，请重新登录")
            location = response
        } else if (success) {
            Class.hideProgress(success, response);
            success(response);
        }
    }

    if (obj.url.indexOf('?') > 0) {
        obj.url = obj.url + "&t=" + new Date().getTime();
    } else {
        obj.url = obj.url + "?t=" + new Date().getTime();
    }

    $.ajax(obj);
}

Class.showProgress = function() {
    if ($('#ajax_wait').length <= 0) {
        var ajax_window = Class.heredoc(function() {
            /*
                        <div class="modal bs-example-modal-sm" id="ajax_wait" data-backdrop="static" data-keyboard="false" ajax_data="1" tabindex="-1" role="dialog" >
                            <div class="modal-dialog modal-sm">
                                <div class="modal-content">
                                    <div class="modal-body">
                                        <img style="position:relative;left:30%" src="../../static/ico/ajax_wait.gif" alt="loading" />
                                    </div>
                                </div>
                            </div>
                        </div>
            */
        });
        $('body').append(ajax_window);
        $('#ajax_wait').modal().css({
            "margin-top": function() {
                return $(this).height() / 2;
            }
        });
    } else {
        $('#ajax_wait').attr('ajax_data', parseInt($('#ajax_wait').attr('ajax_data')) + 1);
    }

    $('#ajax_wait').modal('show');

    var dict = $('#ajax_wait');
    dict.data({
        "min_ajax_time": 500,
        "max_ajax_time": 10000,
        "start_date": new Date()
    });

    var myVar = setInterval(function() {
        var end_date = new Date();
        if (end_date - dict.data('start_date') >= dict.data('max_ajax_time')) {
            $("#ajax_wait").modal('hide');
            clearInterval(myVar);
        }
    }, dict.data('min_ajax_time'));
}

Class.hideProgress = function(success, response) {
    var end_date = new Date();
    var dict = $('#ajax_wait');
    var ajax_time = end_date - dict.data('start_date');
    var ajax_data = parseInt($('#ajax_wait').attr('ajax_data')) - 1;

    if (!$('#ajax_wait').is(':hidden')) {
        if (ajax_time < dict.data('min_ajax_time')) {
            if (ajax_data == 0) {
                setTimeout(function() {
                    $('#ajax_wait').attr('ajax_data', ajax_data);
                    $("#ajax_wait").modal('hide');
                }, (dict.data('min_ajax_time') - ajax_time));
            } else {
                $('#ajax_wait').attr('ajax_data', ajax_data);
            }
        } else if (ajax_time <= dict.data('max_ajax_time')) {
            if (ajax_data == 0) {
                $('#ajax_wait').attr('ajax_data', ajax_data);
                $("#ajax_wait").modal('hide');
            } else {
                $('#ajax_wait').attr('ajax_data', ajax_data);
            }
        } else {
            $("#ajax_wait").modal('hide');
            $('#ajax_wait').attr('ajax_data', 0);
        }
    }
}

Class.heredoc = function(fn) {
    return fn.toString().split('\n').slice(1, -1).join('\n') + '\n'
}

Class.confirm = function(msg, cb) {
    if (confirm(msg || "Are yo sure you want to delete this record?")) {
        cb();
    }
}

Class.csrf = function() {
    return '&csrfmiddlewaretoken=' + $.cookie('csrftoken');
}

Class.JSON = function(obj) {
    if (typeof obj == 'string') {
        return $.parseJSON(obj);
    } else {
        return JSON.stringify(obj);
    }

}

Class.XML = function(obj) {
    if (typeof obj == 'string') {
        return "";
    } else {
        var _toXml = function(list, str) {
            var xml_node = '';
            if (str != 'data') {
                xml_node = "<" + str + "><instance>";
            } else {
                xml_node = "<data>";
            }
            for (var i in list) {
                var dict = list[i];
                for (var key in dict) {
                    var value = dict[key];
                    if (typeof value == 'string' || typeof value == 'number' || typeof value == 'boolean' || value instanceof Date) {
                        xml_node = xml_node + "<" + key + ">" + value + "</" + key + ">";
                    } else if (value instanceof Array) {
                        xml_node = xml_node + _toXml(value, key);
                    }
                }
            }
            if (str != 'data') {
                xml_node = xml_node + "</instance></" + str + ">";
            } else {
                xml_node = xml_node + "</data>";
            }
            return xml_node;
        }
        return _toXml([obj], "data");
    }
}

// query string
Class.Q = function() {
    var vars = {},
        hash, url = window.location.href;
    var hashes = url.slice(url.indexOf('?') + 1).split('&');
    for (var i = 0; i < hashes.length; i++) {
        hash = hashes[i].split('=');
        vars[hash[0]] = hash[1];
    }

    return vars;
}
