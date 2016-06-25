var DatetimeLimit = function() {

    var minTime = (typeof serverTime === 'undefined') ? moment() : serverTime;
    var maxTime = (typeof serverTime === 'undefined') ? moment() : serverTime;

    return {
        setMinTime: function(t) {
            minTime = is.date(t) ? moment(t) : minTime;
        },
        setMaxTime: function(t) {
            maxTime = is.date(t) ? moment(t) : maxTime;
        },
        calcMinTime: function(d) {
            d = is.number(d) ? d : 0;
            minTime.subtract(d, 'days');
        },
        calcMaxTime: function(d) {
            d = is.number(d) ? d : 0;
            maxTime = moment(minTime);
            maxTime.hour(0);
            maxTime.minute(0);
            maxTime.second(0);
            maxTime.millisecond(0);
            maxTime.add(d, 'days');
        },
        getMinTime: function() {
            return moment(minTime);
        },
        getMaxTime: function() {
            return moment(maxTime);
        }
    }
}();
