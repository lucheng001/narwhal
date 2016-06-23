var filterConditions = function() {

    var url = '#';

    var runFilter = function() {
        $('#filter').click(function(){
            var params = {
                currentPage : $('#currentPage').val(),
                currentTeacher : $('#currentTeacher').val(),
                currentSemester : $('#currentSemester').val(),
                currentDepartment : $('#currentDepartment').val(),
                currentSyllabusYear : $('#currentSyllabusYear').val()
            };

            var paramsTplArray = [
                '?',
                'currentPage={currentPage}',
                '&currentTeacher={currentTeacher}',
                '&currentSemester={currentSemester}',
                '&currentDepartment={currentDepartment}',
                '&currentSyllabusYear={currentSyllabusYear}'
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

jQuery(document).ready(function() {
    filterConditions.init();
});