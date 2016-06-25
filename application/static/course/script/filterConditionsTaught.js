var filterConditionsTaught = function() {

    var url = '#';

    var runFilter = function() {
        $('#filter').click(function(){
            var params = {
                currentPage : $('#currentPage').val(),
                currentSemester : $('#currentSemester').val(),
                currentDepartment : $('#currentDepartment').val(),
                currentSyllabusYear : $('#currentSyllabusYear').val()
            };

            var paramsTplArray = [
                '?',
                'currentPage={currentPage}',
                '&currentSemester={currentSemester}',
                '&currentDepartment={currentDepartment}',
                '&currentSyllabusYear={currentSyllabusYear}'
            ];
            var paramsTpl = paramsTplArray.join('');
            window.location.href = url + format(paramsTpl, params);
        });
    };

    return {
        setActionUrl: function(u){
          url = u;
        },
        init: function() {
            runFilter();
        }
    };

}();
