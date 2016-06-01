var data_fields = ['lang_id', 'name', 'description'];
/*
 TODO: alles in één formulier?
 */

$(document).ready(function () {
    var document_id = $('#document_id').val();
    /*$('#save_button').find('button')
        .click(function(){
            save_document();
        });*/

    if (document_id < 0) {
        draw();
    } else {
        draw(get_document(document_id));
    }
    upload_handler(); /* Wat als niet het document, maar enkel de inhoud aangepast wordt? */
});

/*
 * Saving a new document (or an existing one) is done in two steps:
 * 1) Save the document (/api/v2/document), without uploading the file.
 * 2) Upload the file to the saved document (/api/v2/document/id/resource).
 * Afterwards, return something useful.
 */
function save_document() {
    var document_id = $('#document_id').val();
    var form_data = {};
    for (var i = 0; i < data_fields.length; i++) {
        form_data[data_fields[i]] = $('#' + data_fields[i]).val();
    }
    if (document_id > 0) {
        /* Existing document, do nothing */
        return $.ajax({
            url: '/api/v2/document/' + document_id,
            method: 'PUT',
            data: JSON.stringify(form_data),
            success: function (data, status) {
                var document = data.data;
                $('#save_button').html(success_button('Saved'));
            },
            error: function (jqXHR, status, error) {
                $('#save_button').html(error_button(error));
            }
        });
    } else {
        return $.ajax({
            url: '/api/v2/document',
            method: 'POST',
            data: JSON.stringify(form_data),
            success: function (data, status) {
                var document = data.data;
                $('#save_button').html(success_button('Saved'));
                window.location.replace('/admin/document/list');
            },
            error: function (jqXHR, status, error) {
                $('#save_button').html(error_button(error));
            }
        });
    }
}

/**
 * Get a document from the API.
 * @param document_id
 * @returns {*}
 */
function get_document(document_id) {
    return $.ajax({
        url: '/api/v2/document/' + document_id,
        method: 'GET',
        success: function(data, status) {
        },
        error: function (jqXHR, status, error) {
            $('#save_button').html(error_button(error));
        }
    });
}

function draw(deferred) {
    if (deferred == null) {
    } else {
        $.when(deferred).then(function(document_api_response) {
            var document = document_api_response.data;
            for(var i = 0; i < data_fields.length; i++) {
                $('#' + data_fields[i]).val(document[data_fields[i]])
                    .change(function() {
                        $('#save_button').html(default_button('Save'));
                    });
            }
            draw_preview(document.filename, document.mimetype);
        })
    }
}

function upload_handler() {
    $('#input_file').fileupload({
            dataType: 'json',
            add: function (e, data) {
                $('#save_button')
                    .html(default_button('Save'))
                    .find('button').click(function() {
                    $.when(save_document()).then(function(document_api_response) {
                        var document = document_api_response.data;
                        data.url = '/api/v2/document/' + document.id + '/resource';
                        data.submit();
                    })
                });
            },
            done: function(e, data) {
                draw_preview(data.result.data.filename, data.result.data.mimetype);
            }
        });
}

function media_type(mimetype) {
    var split_mimetype = mimetype.split('/');
    return split_mimetype[0];
}

function draw_preview(resource_filename, resource_mimetype) {
    if(media_type(resource_mimetype) != 'image') {
        /* Use jQuery Media */
        $('#current_document').replaceWith('<a class="media" href="/api/v2/resource/' + resource_filename + '" id="current_document"><span class="glyphicon glyphicon-file"></span><span class="sr-only">Attached Document</span></a>');
    } else {
        /* Use img */
        $('#current_document').replaceWith('<img src="/api/v2/resource/' + resource_filename + '" alt="Current document" id="current_document"/>');
    }
    $('#current_document_caption').find('p').html('<em>' + resource_filename + '</em>');
}