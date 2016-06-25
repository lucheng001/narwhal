var Login = function() {

    var handleLogin = function() {

        var formJel = $('#form');
        var errorJel = $('.alert-danger', formJel);

        formJel.validate({
            errorElement: 'span', //default input error message container
            errorClass: 'help-block', // default input error message class
            focusInvalid: false, // do not focus the last invalid input
            rules: {
                userName: {
                    required: true,
                    minlength: 4,
                    maxlength: 16
                },
                password: {
                    required: true,
                    minlength: 6,
                    maxlength: 16
                },
                remember: {
                    required: false
                }
            },

            messages: {
                userName: {
                    required: '用户名不能为空.',
                    minlength: '用户名为4~16个字符.',
                    maxlength: '用户名为4~16个字符.'
                },
                password: {
                    required: '密码不能为空.',
                    minlength: '密码为6~16个字符.',
                    maxlength: '密码为6~16个字符.'
                }
            },

            invalidHandler: function(event, validator) { //display error alert on form submit
                var numberOfErrors = validator.numberOfInvalids();
                if (numberOfErrors) {
                    var errorList = [];
                    for (var i = 0; i < numberOfErrors; i++) {
                        errorList.push(validator.errorList[i].message);
                    }
                    var messages = errorList.join('<br>');
                    $('span', errorJel).html(messages);
                    errorJel.show();
                } else {
                    errorJel.hide();
                }
            },

            highlight: function(element) { // hightlight error inputs
                $(element).closest('.form-group').addClass('has-error'); // set error class to the control group
            },

            success: function(label) {
                label.closest('.form-group').removeClass('has-error');
                label.remove();
            },

            errorPlacement: function(error, element) {
                error.insertAfter(element.closest('.input-icon'));
            },

            submitHandler: function(form) {
                App.blockUI({
                    boxed: true,
                    message: '请稍后...'
                });
                form.submit(); // form validation success, call ajax form submit
            }
        });

        $('.login-form input').keypress(function(e) {
            if (e.which == 13) {
                if ($('.login-form').validate().form()) {
                    $('.login-form').submit(); //form validation success, call ajax form submit
                }
                return false;
            }
        });

    };

    return {
        //main function to initiate the module
        init: function() {
            handleLogin();
        }

    };

}();


jQuery(document).ready(function() {
    Login.init();
});