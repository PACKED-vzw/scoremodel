/**
 * Created by pieter on 17/05/16.
 */


/**
 * Attach a function to all input_type=radio functions
 * to make a request to the API when a user answers
 * a question.
 */
$("input[type*='radio']").change(function(){
    /*
    if put fails: post
    
    get question_answers by user_report
        if question.id in question_answers: PUT; else POST
     perform call on change or save?
     */
});


/**
 * Get this section from the API
 * @param section_id
 * @returns {*}
 */
function section (section_id) {
    return $.ajax({
        method: 'GET',
        url: '/api/v2/section/' + section_id,
        success: function(data, status) {
            /*
            API reply: .data contains all information; .msg contains a status message
             */
            var section = data.data;
            var questions = [];
            for (var i = 0; i < section.questions.length; i++) {
                questions.append();
            }
        },
        error: function(jqXHR, status, error) {}
    });

}


