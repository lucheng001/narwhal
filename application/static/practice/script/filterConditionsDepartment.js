var filterConditionsDepartment = function() {

    var url = '#';

    var runFilter = function() {
        $('#filter').click(function(){
            var params = {
                currentPage : $('#currentPage').val(),
                currentTeacher : $('#currentTeacher').val(),
                currentSemester : $('#currentSemester').val(),
                currentSyllabusYear : $('#currentSyllabusYear').val()
            };

            var paramsTplArray = [
                '?',
                'currentPage={currentPage}',
                '&currentTeacher={currentTeacher}',
                '&currentSemester={currentSemester}',
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
