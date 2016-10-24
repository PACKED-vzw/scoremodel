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
    var parent = element.parent('div');
    /* Setting an error only works on div.form-group */
    while (!parent.hasClass('form-group')) {
        parent = parent.parent('div');
    }
    if (!parent.hasClass('has-error')) {
            /* Prevent the error from appearing multiple times after repeated submits */
            parent
                .addClass('has-error')
                .find('div')
                .append('<span class="help-block">This element is required.</span>');
    }
    var cannot_save = $('#cannot_save');
    if (!cannot_save.hasClass('active')) {
        cannot_save
            .addClass('active')
            .append('<span class="help-block">Form could not be submitted: required elements are missing.</span>');
    }
}

function reset_required_error(selector) {
    var element = $(selector);
    if ($(selector).parent('div').hasClass('has-error')) {
        $(selector).parent('div')
            .removeClass('has-error')
            .find('.help-block').remove();
    }
    var cannot_save = $('#cannot_save');
    if (cannot_save.hasClass('active')) {
        cannot_save
            .removeClass('active')
            .find('.help-block').remove();
    }
}
