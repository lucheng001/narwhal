var changeProfile = function() {

    // basic validation
    var handleValidation = function() {
        // http://docs.jquery.com/Plugins/Validation

        var formJel = $('#form');
        var errorJel = $('.alert-danger', formJel);

        formJel.validate({
            errorElement: 'span', //default input error message container
            errorClass: 'help-block help-block-error', // default input error message class
            focusInvalid: false, // do not focus the last invalid input
            ignore: "", // validate all fields including form hidden input
            rules: {
                chineseName: {
                    required: true,
                    minlength: 2,
                    maxlength: 16
                },
                gender: {
                    required: true
                }
            },

            messages: {
                chineseName: {
                    required: '姓名不能为空.',
                    minlength: '姓名为2~16个字符.',
                    maxlength: '姓名为6~16个字符.'
                },
                gender: {
                    required: '性别不能为空.'
                }
            },

            invalidHandler: function(event, validator) { //display error alert on form submit
                $('span', errorJel).html('填写内容有错误，请仔细检查');
                errorJel.show();
            },

            highlight: function(element) { // hightlight error inputs
                $(element).closest('.form-group').addClass('has-error'); // set error class to the control group
            },

            unhighlight: function(element) { // revert the change done by hightlight
                $(element).closest('.form-group').removeClass('has-error'); // set error class to the control group
            },

            success: function(label) {
                label.closest('.form-group').removeClass('has-error'); // set success class to the control group
            },

            submitHandler: function(form) {
                errorJel.hide();
                App.blockUI({
                    boxed: true,
                    message: '请稍后...'
                });
                form.submit();
            }
        });


    };

    return {
        //main function to initiate the module
        init: function() {
            handleValidation();
        }

    };

}();

jQuery(document).ready(function() {
    changeProfile.init();
});