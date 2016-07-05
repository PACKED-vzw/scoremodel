/**
 * Created by pieter on 5/07/16.
 */

/*
if required and if empty: set
    div.form-group has-warning has-feedback
    input.aria-describedby="id"
    span.class glyphican glyphicon-warning-sign form-control-feedback aria-hidden=true
    span.id id class=sr-only warning
 */


function required_set_side_effects(selectors) {
    var has_error = false;
    for(var i = 0; i < selectors.length; i++) {
        if(required_set(selectors[i])) {
            reset_required_error(selectors[i]);
        } else {
            set_required_error(selectors[i]);
            has_error = true;
        }
    }
    if(has_error) {
        return false;
    } else {
        return true;
    }
}

/**
 * Check whether a required element is set. Return True/False.
 * @param selector
 * @returns boolean
 */
function required_set(selector) {
    var element = $(selector);
    if (
        element.attr('required') &&
        (element.val() == "" ||
        element.val() == undefined)
    ){
        return false;
    }
    return true;
}

function set_required_error(selector) {
    var element = $(selector);
    if (!$(selector).parent('div').hasClass('has-error')) {
            /* Prevent the error from appearing multiple times after repeated submits */
            $(selector).parent('div')
                .attr('class', 'has-error')
                .append('<span class="help-block">This element is required.</span>');
    }
}

function reset_required_error(selector) {
    var element = $(selector);
    if ($(selector).parent('div').hasClass('has-error')) {
        $(selector).parent('div')
            .removeClass('has-error')
            .find('.help-block').remove();
    }
}