Validator = {
    Require: /.+/,
    Email: /^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$/,
    Phone: /^((\(\d{3}\))|(\d{3}\-))?(\(0\d{2,3}\)|0\d{2,3}-)?[1-9]\d{6,7}$/,
    Mobile: /^((\(\d{3}\))|(\d{3}\-))?13\d{9}$/,
    Url: /^(http:|https:)\/\/[A-Za-z0-9]+\.[A-Za-z0-9]+[\/=\?%\-&_~`@[\]\':+!]*([^<>\"\"])*$/,
    IdCard: /^\d{15}(\d{2}[A-Za-z0-9])?$/,
    Currency: /^\d+(\.\d+)?$/,
    Number: /^\d+$/,
    Zip: /^[1-9]\d{5}$/,
    QQ: /^[1-9]\d{4,8}$/,
    Integer: /^[-\+]?\d+$/,
    Double: /^[-\+]?\d+(\.\d+)?$/,
    English: /^[A-Za-z]+$/,
    Chinese: /^[\u0391-\uFFE5]+$/,
    UnSafe: /^(([A-Z]*|[a-z]*|\d*|[-_\~!@#\$%\^&\*\.\(\)\[\]\{\}<>\?\\\/\'\"]*)|.{0,5})$|\s/,
    IsSafe: function(str) {
        return !this.UnSafe.test(str);
    },
    SafeString: "this.IsSafe(value)",
    Limit: "this.limit(value.length,getAttribute('min'),  getAttribute('max'))",
    LimitB: "this.limit(this.LenB(value), getAttribute('min'), getAttribute('max'))",
    Date: "this.IsDate(value, getAttribute('min'), getAttribute('format'))",
    Repeat: "value == document.getElementsByName(getAttribute('to'))[0].value",
    Range: "getAttribute('min') < value && value < getAttribute('max')",
    Compare: "this.compare(value,getAttribute('operator'),getAttribute('to'))",
    Custom: "this.Exec(value, getAttribute('regexp'))",
    Group: "this.MustChecked(getAttribute('name'), getAttribute('min'), getAttribute('max'))",
    ErrorItem: [document.forms[0]],
    ErrorMessage: ["以下原因导致提交失败：\t\t\t\t"],
    init: function(theForm, validate_obj) {
        var form_obj = theForm;
        $.each(validate_obj, function(key, value) {
            form_obj.find('[name=' + key + ']').tooltip({
                title: value.msg,
                trigger: 'manual'
            }).blur(value, Validator.validate)
        });
    },
    validate: function(event) {
        validator_obj = event.data;
        if (Validator[validator_obj.type]) {
            if (!Validator[validator_obj.type]($(this).val(), validator_obj)) {
                $(this).tooltip('show');
            } else {
                $(this).tooltip('hide');
            }
        }
    },
    string: function(value, validator_obj) {
        if (value.length < validator_obj.max && value.length > validator_obj.min) {
            return true;
        } else {
            return false
        }
    },
    email: function(value, validator_obj) {
        
    },
    LenB: function(str) {
        return str.replace(/[^\x00-\xff]/g, "**").length;
    },
    ClearState: function(elem) {
        with(elem) {
            if (style.color == "red")
                style.color = "";
            var lastNode = parentNode.childNodes[parentNode.childNodes.length - 1];
            if (lastNode.id == "__ErrorMessagePanel")
                parentNode.removeChild(lastNode);
        }
    },
    AddError: function(index, str) {
        this.ErrorItem[this.ErrorItem.length] = this.ErrorItem[0].elements[index];
        this.ErrorMessage[this.ErrorMessage.length] = this.ErrorMessage.length + ":" + str;
    },
    Exec: function(op, reg) {
        return new RegExp(reg, "g").test(op);
    },
    compare: function(op1, operator, op2) {
        switch (operator) {
            case "NotEqual":
                return (op1 != op2);
            case "GreaterThan":
                return (op1 > op2);
            case "GreaterThanEqual":
                return (op1 >= op2);
            case "LessThan":
                return (op1 < op2);
            case "LessThanEqual":
                return (op1 <= op2);
            default:
                return (op1 == op2);
        }
    },
    MustChecked: function(name, min, max) {
        var groups = document.getElementsByName(name);
        var hasChecked = 0;
        min = min || 1;
        max = max || groups.length;
        for (var i = groups.length - 1; i >= 0; i--)
            if (groups[i].checked) hasChecked++;
        return min <= hasChecked && hasChecked <= max;
    },
    IsDate: function(op, formatString) {
        formatString = formatString || "ymd";
        var m, year, month, day;
        switch (formatString) {
            case "ymd":
                m = op.match(new RegExp("^((\\d{4})|(\\d{2}))([-./])(\\d{1,2})\\4(\\d{1,2})$"));
                if (m == null) return false;
                day = m[6];
                month = m[5]--;
                year = (m[2].length == 4) ? m[2] : GetFullYear(parseInt(m[3], 10));
                break;
            case "dmy":
                m = op.match(new RegExp("^(\\d{1,2})([-./])(\\d{1,2})\\2((\\d{4})|(\\d{2}))$"));
                if (m == null) return false;
                day = m[1];
                month = m[3]--;
                year = (m[5].length == 4) ? m[5] : GetFullYear(parseInt(m[6], 10));
                break;
            default:
                break;
        }
        if (!parseInt(month)) return false;
        month = month == 12 ? 0 : month;
        var date = new Date(year, month, day);
        return (typeof(date) == "object" && year == date.getFullYear() && month == date.getMonth() && day == date.getDate());

        function GetFullYear(y) {
            return ((y < 30 ? "20" : "19") + y) | 0;
        }
    }
}
