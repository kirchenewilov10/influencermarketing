function onclick_create_campaign() {
    window.location.href = '/create_campaign';
}

// *************** Get Cookie *************** //
function getCooke(name) {
	var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// *************** Get CSRF Token *************** //
function getCsrfToken() {
	return getCooke("csrftoken");
}

$( document ).ajaxSend(function( event, jqxhr, settings ) {
    jqxhr.setRequestHeader("X-CSRFToken", getCsrfToken());
});