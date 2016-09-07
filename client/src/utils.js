import $ from 'jquery';

function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function getCSRF() {
    var csrftoken = readCookie('csrftoken')
    if (csrftoken == null) {
        csrftoken = $('#csrf_token').val()
    }
    return csrftoken;
}

function isToday(date) {
    var currentDate = new Date();
    if (date.getFullYear() !== currentDate.getFullYear()) {
        return false;
    }
    if (date.getMonth() !== currentDate.getMonth()) {
        return false;
    }
    if (date.getDate() !== currentDate.getDate()) {
        return false;
    }
    return true;
}

export {readCookie, getCSRF, isToday};