/**
 * Created by pieter on 6/07/16.
 */

/*
Register two event handles to the save button:
1) upload the document
2) save the data

Always do (2) first!
 */

/*
Add require!
 */
$(document).ready(function () {
    $('#description').markdown({
        fullscreen: {
            enable: false
        },
        hiddenButtons: [
            'Preview'
        ]
    });

    /*
    On the 'add' event: check whether this document already exists. If it does,
    upload the file and wait till the user clicks 'Save'. If it doesn't,
    save the document, upload the file and switch to the edit form.
     */
    $('#input_file').fileupload({
        dataType: 'json',
        add: function(e, data) {
            default_button('#save_button', 'Save');
            $('#progress_indicator').find('div').remove();
            var document_id = $('#document_id').val();
            if (document_id < 0) {
                /* If document_id < 0: save document, get id and submit */
                /*
                   We need to save the document first, as the API does not accept
                   files ('resources') that are not linked to an existing document.
                 */
                if (required_set_side_effects(['#lang_id', '#name'])) {
                    $.when(save_document_data()).then(
                        function success (document_api_response) {
                            var document_id = document_api_response.data.id;
                            data.url = '/api/v2/document/' + document_id + '/resource';
                            data.submit();
                        },
                        function error(jqXHR, status, error) {
                            error_button('#save_button', error);
                        }
                    );
                }
            } else {
                /* Else: submit: saving the document is only after click on submit */
                data.url = '/api/v2/document/' + document_id + '/resource';
                data.submit();
            }
        },
        done: function(e, data) {
            var progress_indicator = $('#progress_indicator');
            progress_indicator.find('div').remove();
            progress_indicator.append('<div class="btn btn-success" role="alert"><span class="glyphicon glyphicon-ok" aria-hidden="true"></span><span class="sr-only">Upload successful</span></div>');
            var uploaded = data.result.data;
            var document_id = $('#document_id').val(); /* The old, lesser than 0 document_id */
            if (document_id < 0) {
                /* Now redirect to the edit form */
                window.location.replace('/admin/document/edit/' + uploaded.linked_id);
            } else {
                /* Stay here */
                draw_preview(uploaded.filename, uploaded.mimetype);
            }
        },
        start: function(e, data) {
            var progress_indicator = $('#progress_indicator');
            progress_indicator.append('<div class="progress"><div id="progress_bar" class="progress-bar" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0;"><span class="sr-only">0% Complete</span></div></div>');
        },
        progress: function(e, data) {
            var progress = parseInt(data.loaded / data.total * 100, 10);
            var progress_bar = $('#progress_bar');
            progress_bar
                .attr('aria-valuenow', progress)
                .css('width', progress + '%');
            progress_bar.parent('div').find('.sr-only').text(progress + '% Complete');
        },
        fail: function(e, data) {
            error_button('#save_button', data.textStatus);
        }
    });
    if ($('#document_id').val() < 0) {
        /* A new document, no data from the API */
        draw(null, true);
    } else {
        draw(get_document_data(), true);
    }
});

/**
 * Save the data from the document (not the file!).
 * @returns {*}
 */
function save_document_data() {
    var document_id = $('#document_id').val();
    var form_data = {
        'lang_id': $('#lang_id').val(),
        'name': $('#name').val(),
        'description': $('#description').val()
    };
    var url;
    var method;
    if (document_id < 0) {
        /* New document */
        url = '/api/v2/document';
        method = 'POST';
    } else {
        /* Existing document */
        url = '/api/v2/document/' + document_id;
        method = 'PUT';
    }
    return $.ajax({
        url: url,
        method: method,
        data: JSON.stringify(form_data),
        success: function(data, status) {
            success_button('#save_button', 'Saved');
        },
        error: function(jqXHR, status, error) {
            error_button('#save_button', error);
        }
    });
}

/**
 * Get document data from the API.
 * @returns {*}
 */
function get_document_data() {
    var document_id = $('#document_id').val();
    return $.ajax({
        url: '/api/v2/document/' + document_id,
        method: 'GET',
        success: function(data, status) {},
        error: function(jqXHR, status, error) {
            error_button('#save_button', error);
        }
    });
}

/**
 * Insert the data we got from the api (deferred) into the form.
 * @param deferred
 * @param is_first_time
 */
function draw(deferred, is_first_time) {
    if (deferred) {
        $.when(deferred).then(function(document_api_response) {
            var document = document_api_response.data;
            $('#lang_id').val(document.lang_id);
            $('#name').val(document.name);
            $('#description').val(document.description);
            $('#document_id').val(document.id);
            draw_preview(document.filename, document.mimetype);
        });
    }
    if (is_first_time) {
        /* Add change handlers */
        var fields = ['lang_id', 'name', 'description'];
        for (var i = 0; i < fields.length; i++) {
            $('#' + fields[i]).focus(function(){
                default_button('#save_button', 'Save');
            });
        }
        /* Add click handler to save button */
        $('#save_button').click(function() {
            if (required_set_side_effects(['#lang_id', '#name'])) {
                draw(save_document_data());
            }
        });
    }
}

function media_type(mimetype) {
    var split_mimetype = mimetype.split('/');
    return split_mimetype[0];
}

/**
 * Draw a preview of the uploaded file.
 * @param resource_filename
 * @param resource_mimetype
 */
function draw_preview(resource_filename, resource_mimetype) {
    if(media_type(resource_mimetype) != 'image') {
        $('#current_document').replaceWith('<a class="media" href="/api/v2/resource/' + resource_filename + '" id="current_document"><span class="glyphicon glyphicon-file"></span><span class="sr-only">Attached Document</span></a>');
    } else {
        /* Use img */
        $('#current_document').replaceWith('<img src="/api/v2/resource/' + resource_filename + '" alt="Current document" id="current_document"/>');
    }
    $('#current_document_caption').find('p').html('<em>' + resource_filename + '</em>');
}