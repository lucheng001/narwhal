var deleteCourse = function() {

    var actionUrl = '';
    var objId = '';

    var bindEvent = function() {
        $('a.deleteCourse').click(function(e) {
            objId = $(this).attr('data-courseId');
            handleAction();
            e.preventDefault();
        });
    };

    var handleAction = function() {
        bootbox.dialog({
            message: '确认删除该课程吗？',
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

jQuery(document).ready(function() {
    deleteCourse.init();
});