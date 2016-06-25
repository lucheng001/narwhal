var GeoLocation = function() {


    var positionSuccess = function(position) {
        var latitude = position.coords.latitude;
        var longitude = position.coords.longitude;
        var accuracy = position.coords.accuracy;
        $('input[name=latitude]').val(latitude);
        $('input[name=longitude]').val(longitude);

        $('p.geoLatitude').html('纬度：' + latitude);
        $('p.geoLongitude').html('经度：' + longitude);

    };

    var positionError = function(error) {
        var errorTypes = {
            1: '没有权限获取定位数据.', // permission denied
            2: '获取定位数据失败.', //position unavailable
            3: '获取定位数据超时.' // timeout
        };
        bootbox.dialog({
            message: errorTypes[error.code],
            title: '错 误',
            buttons: {
                confirm: {
                    label: '确 认',
                    className: 'blue',
                    callback: function() {}
                },
                cancel: {
                    label: '取 消',
                    className: 'default',
                    callback: function() {}
                }
            }
        });
    };

    return {
        init: function() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(positionSuccess, positionError, {
                    enableHighAccuracy: true,
                    timeout: 5000,
                });
            } else {
                bootbox.dialog({
                    message: '浏览器不支持GPS定位，请更换浏览器后再试.',
                    title: '错 误',
                    buttons: {
                        confirm: {
                            label: '确 认',
                            className: 'blue',
                            callback: function() {}
                        },
                        cancel: {
                            label: '取消',
                            className: 'default',
                            callback: function() {}
                        }
                    }
                });
            }
        }
    }
}();

jQuery(document).ready(function() {
    GeoLocation.init();
});