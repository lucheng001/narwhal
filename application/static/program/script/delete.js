var deleteProgram = function() {

    var actionUrl = '';
    var objId = '';

    var bindEvent = function() {
        $('button.deleteProgram').click(function(e) {
            objId = $(this).attr('data-programId');
            handleAction();
            e.preventDefault();
        });
    };

    var handleAction = function() {
        bootbox.dialog({
            message: '确认删除该培养方案吗？',
            title: '通 知',
            buttons: {
                confirm: {
                    label: '确 认',
                    className: 'blue',
                    callback: function() {
                        window.location.href = actionUrl + objId;
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
