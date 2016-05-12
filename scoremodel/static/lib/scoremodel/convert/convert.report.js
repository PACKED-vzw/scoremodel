/**
 * Created by pieter on 5/01/16.
 */

var ConvertReport = function() {

};

ConvertReport.prototype.from_api = function(data, available_answers, available_risk_factors) {
    /*
    Assigning an object to a variable copies a reference, not the object. Using angular.copy ensures
    that data.sections does not get removed when we get the IDs.
     */
    var output_data = angular.copy(data.data.data);
    /*
    For every question in every section, add answer_selected and risk_factor_selected
    so that for every possible answer/risk_factor the following holds:
    if answer in question.answers:
        question.answer_selected[answer.id] = true
    else:
        question.answer_selected[answer.id] = false
     */
    /*
    Used for the initial _get_; this function is not very useful afterwards
     */
    for (var i = 0; i < output_data.sections.length; i++) {
        var section = output_data.sections[i];
        for (var j = 0; j < section.questions.length; j++) {
            /*
            Set question.risk_factors to risk_factors[x] where risk_factors[x].id == question.risk_factors[0].id
             */
            var question = section.questions[j];
            if (question.risk_factor_id) {
                /* If it's empty, nothing to set */
                for (var k = 0; k < available_risk_factors.length; k++) {
                    var possible_risk_factor = available_risk_factors[k];
                    if (possible_risk_factor.id == question.risk_factor_id) {
                        output_data.sections[i].questions[j].risk_factor = possible_risk_factor;
                        break;
                    }
                }
            }
        }
    }
    return output_data;
};

ConvertReport.prototype.to_api = function(data) {
    var required_params = ['title'];
    var complex_params = [];
    var cleaned_data = CheckForRequiredParams(data, required_params, complex_params);
    cleaned_data.sections = undefined; // Sections are stored 'atomically'
    return cleaned_data;
};
