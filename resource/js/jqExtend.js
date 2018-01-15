$.fn.Val = function(value) {
    if (!value && value != '') {
        return false
    };

    var me = $(this);

    if (me.is(":text") || me.is("textarea")) {
        me.val(value).blur();
    } else if (me.is("select")) {
        me.val(value).change();
    } else if (me.is(":radio") || me.is(":checkbox")) {
        if ((me.val() == "1" || me.val() == "0") && (value == "True" || value == "False")) {
            value = value == "True" ? 1 : 0;
        }
        if (me.val() == value) {
            me.attr("checked", true);
        } else {
            me.removeAttr("checked");
        }
        me.change();
    } else if (me.is("label")) {
        me.html(value);
    } else if (me.is("td")) {
        me.text(value);
    }

    return me
};

$.fn.Param = function(obj, return_type) {
    if (obj) {
        if (typeof obj == "string")
            obj = $.parseJSON(obj);
        for (var prop in obj) {
            $('[name=' + prop + ']', this).each(function() {
                $(this).Val(obj[prop]);
            });
        }
    } else {
        var param_obj = {};
        this.find("input[type=text], textarea, select").each(function() {
            if ($(this).is(":visible")) {
                param_obj[this.name] = $(this).val();
            }
        });

        this.find("input[type=checkbox]").each(function() {
            if ($(this).is(":visible")) {
                param_obj[this.name] = ($(this).is(":checked") ? 1 : 0);
            }
        });

        this.find("input[type=radio]").each(function() {
            if ($(this).is(":visible")) {
                if ($(this).is(":checked")) {
                    param_obj[this.name] = $(this).val();
                }
            }
        });

        this.find("input[type=hidden]").each(function() {
            param_obj[this.name] = $(this).val();
        });

        if (return_type) {
            return param_obj;
        }
        return $.param(param_obj);
    }
};

$.fn.ParamEX = function(obj) {
    if (obj) {
        if (typeof obj == "string") {
            obj = $.parseJSON(obj);
        }

        for (var p in obj) {
            var prop = obj[p];
            if (typeof prop == 'string' || typeof prop == 'number' || typeof prop == 'boolean' || prop instanceof Date) {
                $('[name=' + p + ']', this).each(function() {
                    if ($(this).parents("div[instance=1]").length == 0) {
                        $(this).Val(prop);
                    }
                });
            } else if (prop instanceof Array) {
                first = $('div[instance=1][name=' + p + ']', this).eq(0);
                $('div[instance=1][name=' + p + ']:gt(0)', this).remove();
                for (var i = 0; i < prop.length; i++) {
                    if (i == 0) {
                        first.Param(prop[i])
                    } else {
                        first.clone().Reset().insertAfter($('div[instance=1][name=' + p + ']', this).last()).Param(prop[i]);
                    }
                }
            }
        }

        return this;
    } else {
        var obj = {};
        var self = $(this);

        self.find("div[instance=1]").each(function() {
            var self = $(this);
            if (!obj[self.attr('name')]) {
                obj[self.attr('name')] = [];
            }

            obj[self.attr('name')].push(self.Param(null, 1));
        });

        self.find("input[type=text], textarea, select").each(function() {
            if ($(this).is(":visible") && $(this).parents("div[instance=1]").length == 0) {
                obj[this.name] = $(this).val();
            }
        });

        self.find("input[type=checkbox]").each(function() {
            if ($(this).is(":visible") && $(this).parents("div[instance=1]").length == 0) {
                obj[this.name] = ($(this).is(":checked") ? 1 : 0);
            }
        });

        self.find("input[type=radio]").each(function() {
            if ($(this).is(":visible") && $(this).parents("div[instance=1]").length == 0) {
                if ($(this).is(":checked") && $(this).parents("div[instance=1]").length == 0) {
                    obj[this.name] = $(this).val();
                }
            }
        });

        self.find("input[type=hidden]").each(function() {
            if ($(this).parents("div[instance=1]").length == 0) {
                obj[this.name] = $(this).val();
            }
        });

        return obj;
    }
};

$.fn.Reset = function() {
    var self = this;
    $("textarea,:text,:password,input[type=email],input[type=hidden]", self).each(function() {
        $(this).val("");
    });

    $("select", self).each(function() {
        $(this).val("");
        $(this).change();
    });

    $(":radio,:checkbox", self).each(function() {
        $(this).attr("checked", false);
        $(this).change();
    });

    $.each(self.data(), function(key, value) {
        if (/^ms_.+$/.test(key)) {
            self.removeData(key);
        }
    })

    return self;
};
