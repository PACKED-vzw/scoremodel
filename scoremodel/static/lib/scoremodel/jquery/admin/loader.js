
function add_loader(selector) {
    $(selector).append('<span id="loader_gif"><img src="/static/img/reload.gif" height="20px"></span>');
}

function remove_loader(selector) {
    if (async_counter == 0) {
        $(selector).find('#loader_gif').remove();
    }
}

function increment_counter() {
    async_counter = async_counter + 1;
}

function decrement_counter() {
    async_counter = async_counter - 1;
}
