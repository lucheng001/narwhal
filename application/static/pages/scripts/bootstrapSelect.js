var BootstrapSelect = function () {

    var handleBootstrapSelect = function() {
        $('.bs-select').selectpicker({
            iconBase: 'fa',
            tickIcon: 'fa-check'
        });
    }

    return {
        //main function to initiate the module
        init: function () {      
            handleBootstrapSelect();
        }
    };

}();

jQuery(document).ready(function() {
    BootstrapSelect.init();
});
