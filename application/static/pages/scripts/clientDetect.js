var ClientDetect = function() {
    return {
        init: function() {
            $('input[name=deviceName]').val(detector.device.name);
            $('input[name=osName]').val(detector.os.name);
            $('input[name=osVersion]').val(detector.os.fullVersion);
            $('input[name=browserName]').val(detector.browser.name);
            $('input[name=browserVersion]').val(detector.browser.fullVersion);
            $('input[name=engineName]').val(detector.engine.name);
            $('input[name=engineVersion]').val(detector.engine.fullVersion);
        }
    }
}();

jQuery(document).ready(function() {
    ClientDetect.init();
});