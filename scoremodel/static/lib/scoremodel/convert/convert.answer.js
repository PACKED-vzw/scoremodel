/**
 * Created by pieter on 5/01/16.
 */

var ConvertAnswer = function(data) {
    this.input_data = data.data.data;
};

ConvertAnswer.prototype.from_api = function() {
    return this.input_data;
};
