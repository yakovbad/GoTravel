var BASEURL = "/api/v1/";
var TIMEOUT = 30000;

function get(url, data, success) {
    $.ajax({
        url: BASEURL + url,
        type: "GET",
        data: data,
        success:success
    });
}


function post(url, data, success) {
    data['csrfmiddlewaretoken'] = $.cookie().csrftoken;
    $.ajax({
        url: BASEURL + url,
        type: "POST",
        data: data,
        success:success
    });
}