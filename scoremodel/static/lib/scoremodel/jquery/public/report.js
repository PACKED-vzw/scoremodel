/**
 * Created by pieter on 18/05/16.
 */

$(document).ready(function() {
});

function data_for_table() {
    var scores = $('span').filter(function(){
        if ($(this).attr('id')) {
            return true;
        }
    });
}