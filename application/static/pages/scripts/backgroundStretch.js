var BackgroundStretch = function() {

    return {
        //main function to initiate the module
        init: function() {

            // init background slide images
            $('.login-bg').backstretch([
                '/static/pages/img/bg1.jpg',
                '/static/pages/img/bg2.jpg',
                '/static/pages/img/bg3.jpg'
            ], {
                fade: 1000,
                duration: 8000
            });
        }
    };

}();

jQuery(document).ready(function() {
    BackgroundStretch.init();
});