/**
 * Created by pieter on 5/01/16.
 */

var ConvertSection = function() {

};

ConvertSection.prototype.from_api = function(data) {
    /*
    Never used for initial fetch; section.questions is removed and replaced with whatever already exists,
    so there is no need to parse/clean anything.
     */
    return angular.copy(data.data.data);
};

ConvertSection.prototype.to_api = function(data, report_id) {
    var required_params = ['title', 'total_score'];
    var complex_params = [];
    var cleaned_data = CheckForRequiredParams(data, required_params, complex_params);
    cleaned_data.questions = undefined; // Questions are stored 'atomically'
    cleaned_data.report_id = report_id;
    if (cleaned_data.id < 0) {
        cleaned_data.id = undefined;
    }
    return cleaned_data;
};

