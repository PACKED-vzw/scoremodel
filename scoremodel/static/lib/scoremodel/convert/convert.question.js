/**
 * Created by pieter on 5/01/16.
 */

var ConvertQuestion = function() {
};

ConvertQuestion.prototype.from_api = function(data, available_risk_factors) {
    var output_data = angular.copy(data.data.data);
    if (output_data.risk_factors.length >= 1) {
        /* If it's empty, nothing to set */
        for (var k = 0; k < available_risk_factors.length; k++) {
            var possible_risk_factor = available_risk_factors[k];
            if (possible_risk_factor.id == output_data.risk_factors[0].id) {
                output_data.risk_factors = possible_risk_factor;
                break;
            }
        }
    }
    return output_data;
};

ConvertQuestion.prototype.to_api = function(data, section_id) {
    /**
     * Convert input_data to api_data.
     * risk_factors: array of risk_factor objects as returned by the API.
     * answers: array of answer objects as retunred by the API.
     */
    var required_params = ['answers', 'weight', 'order_in_section', 'risk', 'context', 'question', 'example', 'action', 'risk_factors'];
    var complex_params = ['answers', 'risk_factors'];
    var cleaned_data = CheckForRequiredParams(data, required_params, complex_params);
    cleaned_data.section_id = section_id;
    if (cleaned_data.id < 0) {
        cleaned_data.id = undefined;
    }
    /*
    Do not use json.stringify: this will create a JSON string representation, but that is then json-stringified again
    by $http.post() etc.
     */
    cleaned_data.risk_factors = this.get_selected_risk_factor(cleaned_data.risk_factors);
    /* Answers are already in an array because we use select multiple */
    console.log('data');
    console.log(cleaned_data);
    return cleaned_data;
};

ConvertQuestion.prototype.get_selected_risk_factor = function(risk_factor) {
    /**
     * input_data.risk_factors is the selected risk factor, but it must be in an array
     */
    return [risk_factor];
};

