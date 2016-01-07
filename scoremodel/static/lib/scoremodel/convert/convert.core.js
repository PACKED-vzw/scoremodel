/**
 * Created by pieter on 5/01/16.
 */


function in_array(input_array, item) {
    if (input_array.indexOf(item) != -1) {
        return true;
    } else {
        return false;
    }
}

function CheckForRequiredParams(input_data, required_params, complex_params) {
    /**
     * Checks input data for all attributes in required params. If one is missing
     * set it to '' or to [] if it is in complex_params.
     */
    var output_data = angular.copy(input_data);
    for(var i = 0; i < required_params.length; i++) {
        var required_param = required_params[i];
        if (!output_data.hasOwnProperty(required_param)) {
            if (in_array(complex_params, required_param)) {
                output_data[required_param] = [];
            } else {
                output_data[required_param] = '';
            }
        }
    }
    return output_data;
}
