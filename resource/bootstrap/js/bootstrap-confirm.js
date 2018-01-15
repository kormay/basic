(function($) {
    $.extend({
        confirm: function(msg, fn) {
            var result = false;
            if ($("#system_confirm").length == 0) {
                var html = "<div id='system_confirm' tabindex='-1' class='modal fade' role='dialog' aria-labelledby='jconfirm_title'> <div class='modal-dialog'> <div class='modal-content'> <div class='modal-header'> <button type='button' class='close' data-dismiss='modal' aria-label='Close'><span aria-hidden='true'>&times;</span></button> <h4 class='modal-title' id='confirm_title'></h4> </div> <div class='modal-body' id='confirm_message'> </div> <div class='modal-footer'> <button id='confirm_yes' type='button' class='btn btn-primary'>Yes</button> <button id='cancel' type='button' class='btn btn-primary' data-dismiss='modal'>No</button> </div> </div> </div> </div>";
                $("body").append(html);
                $("#confirm_yes").on('click', function() {
                    result = true;
                    $("#system_confirm").modal("hide");
                    if (fn && typeof fn == "function") {
                        fn(result);
                    }
                });
            }
            if (msg && msg.length > 0) {
                $("#confirm_message").html(msg);
            }

            $("#system_confirm").modal({ backdrop: 'static', show: true });
        }
    });
})(jQuery);
