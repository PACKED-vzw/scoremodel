$(document).ready(function(){
    var page_id = $('#page_id').val();
    draw(get_page(page_id));

    /* Bootstap Markdown */
    $('#content').markdown({
        fullscreen: {
            enable: false
        },
        hiddenButtons: [
            'Preview'
        ]
    });
});

/**
 * Save the current page. Return a deferred.
 * @param page_id
 * @returns {*}
 */
function save_page(page_id) {
    var page_data = {
        lang_id: parseInt($('#lang_id').val()),
        menu_link_id: parseInt($('#menu_link_id').val()),
        content: $('#content').val()
    };
    return $.ajax({
        method: 'PUT',
        url: '/api/v2/page/' + page_id,
        data: JSON.stringify(page_data),
        success: function(data, status) {
            success_button('#save_button', 'Saved');
        },
        error: function(jqXHR, status, error) {
            error_button('#save_button', error);
        }
    });
}

/**
 * Draw the current page, using the form provided in HTML.
 * Takes a deferred ($.ajax()) as input.
 * Sets the .onclick event on the save button.
 * @param deferred
 */
function draw(deferred) {
    $.when(deferred).then(function(page_api_resp) {
        var page = page_api_resp.data;
        $('#lang').attr('value', page.lang);
        $('#lang_id').attr('value', page.lang_id);
        $('#menu_link').attr('value', page.menu_link);
        $('#menu_link_id').attr('value', page.menu_link_id);
        $('#content')
            .val(page.content)
            .change(function(){
                $('#save_button')
                    .click(function(){
                        var page_id = $('#page_id').val();
                        draw(save_page(page_id));
                    });
                default_button('#save_button', 'Save');
            });
        $('#save_button')
            .click(function(){
                var page_id = $('#page_id').val();
                draw(save_page(page_id));
            });
    });
}

/**
 * Get a page (by page_id).
 * Returns a deferred.
 * @param page_id
 * @returns {*}
 */
function get_page(page_id) {
    return $.ajax({
        method: 'GET',
        url: '/api/v2/page/' + page_id,
        success: function(data, status) {},
        error: function(jqXHR, status, error) {
            error_button('#save_button', error);
        }
    });
}
