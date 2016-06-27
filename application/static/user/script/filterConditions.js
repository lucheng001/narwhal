var filterConditions = function() {

    var url = '#';

    var runFilter = function() {
        $('#filter').click(function(){
            var params = {
                currentPage : $('#currentPage').val(),
                currentGender : $('#currentGender').val(),
                currentRole : $('#currentRole').val(),
            };

            var paramsTplArray = [
                '?',
                'currentPage={currentPage}',
                '&currentGender={currentGender}',
                '&currentRole={currentRole}'
            ];
            var paramsTpl = paramsTplArray.join('');
            window.location.href = url + format(paramsTpl, params);
        });
    };

    return {
        setUrl: function(u){
          url = u;
        },
        init: function() {
            runFilter();
        }
    };

}();
