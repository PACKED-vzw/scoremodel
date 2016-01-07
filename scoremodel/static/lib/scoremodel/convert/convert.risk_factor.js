/**
 * Created by pieter on 5/01/16.
 */

var ConvertRiskFactor = function(data) {
    this.input_data = data.data.data;
};

ConvertRiskFactor.prototype.from_api = function() {
    return this.input_data;
};
