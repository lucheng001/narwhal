var addByBatch = function() {

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
                practiceData: {
                    required: true
                }
            },

            messages: {
                practiceData: {
                    required: '实训数据不能为空.'
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
    addByBatch.init();
});