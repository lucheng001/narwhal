var ActiveMenu = function() {

    var aJels = $('a.nav-link');
    var currentPathName = window.location.pathname;

    return {
        init: function() {
            for (var i = 0; i < aJels.length; i++) {
                var pathname = aJels[i].pathname;
                var aJel = $(aJels[i]);
                var href = aJel.attr('href');

                if (href.indexOf(currentPathName) == 0) {
                    var parentLiJel = aJel.parent('.nav-item');
                    parentLiJel.addClass('active');
                    break;
                }

            }
        }
    }
}();

jQuery(document).ready(function() {
    ActiveMenu.init();
});