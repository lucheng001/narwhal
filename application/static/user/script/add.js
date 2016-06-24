var addUser = function() {

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
                userName: {
                    required: true,
                    minlength: 4,
                    maxlength: 16
                },
                chineseName: {
                    required: true,
                    maxlength: 16
                },
                password: {
                    required: true,
                    minlength: 6,
                    maxlength: 16
                },
                confirmPassword: {
                    required: true,
                    equalTo: '#password',
                    minlength: 6,
                    maxlength: 16
                },
                gender: {
                    required: true
                },
                role: {
                    required: true
                }
            },

            messages: {
                userName: {
                    required: '用户名不能为空.',
                    minlength: '用户名为4~16个字符.',
                    maxlength: '用户名为4~16个字符.'
                },
                chineseName: {
                    required: '姓名不能为空.',
                    maxlength: '姓名最初为16个字符.'
                },
                password: {
                    required: '密码不能为空.',
                    minlength: '密码为6~16个字符.',
                    maxlength: '密码为6~16个字符.'
                },
                confirmPassword: {
                    required: '确认密码不能为空.',
                    equalTo: '确认密码和密码不一致.',
                    minlength: '确认密码为6~16个字符.',
                    maxlength: '确认密码为6~16个字符.'
                },
                gender: {
                    required: '性别不能为空.'
                },
                role: {
                    required: '角色不能为空.'
                }
            },

            errorPlacement: function(error, element) { // render error placement for each input type
                if (element.parent('.input-group').size() > 0) {
                    error.insertAfter(element.parent('.input-group'));
                } else if (element.attr('data-error-container')) {
                    error.appendTo(element.attr('data-error-container'));
                } else if (element.parents('.radio-list').size() > 0) {
                    error.appendTo(element.parents('.radio-list').attr('data-error-container'));
                } else if (element.parents('.radio-inline').size() > 0) {
                    error.appendTo(element.parents('.radio-inline').attr('data-error-container'));
                } else if (element.parents('.checkbox-list').size() > 0) {
                    error.appendTo(element.parents('.checkbox-list').attr('data-error-container'));
                } else if (element.parents('.checkbox-inline').size() > 0) {
                    error.appendTo(element.parents('.checkbox-inline').attr('data-error-container'));
                } else {
                    error.insertAfter(element); // for other inputs, just perform default behavior
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
    addUser.init();
});