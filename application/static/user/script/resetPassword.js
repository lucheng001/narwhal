var resetPassword = function() {

    var actionUrl = '';
    var objId1 = '';
    var objId2 = '';

    var bindEvent = function() {
        $('button.resetPassword').click(function(e) {
            objId1 = $(this).attr('data-courseId');
            objId2 = $(this).attr('data-studentId');
            handleAction();
            e.preventDefault();
        });
    };

    var handleAction = function() {
        bootbox.dialog({
            message: '确认重置该同学的密码吗？',
            title: '通 知',
            buttons: {
                confirm: {
                    label: '确 认',
                    className: 'blue',
                    callback: function() {
                        var params = format('{}/{}', objId1, objId2)
                        window.location.href = actionUrl + params;
                    }
                },
                cancel: {
                    label: '取消',
                    className: 'default',
                    callback: function() {}
                }
            }
        });
    };

    return {
        //main function to initiate the module
        init: function() {
            bindEvent();
        },
        setActionUrl: function(url) {
            actionUrl = url
        }
    };

}();
