
// helper function to set cookies
function setCookie(cname, cvalue, seconds) {
    var d = new Date();
    d.setTime(d.getTime() + (seconds * 1000));
    var expires = "expires="+ d.toUTCString();
    document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}

// helper function to get a cookie
function getCookie(cname) {
    var name = cname + "=";
    var decodedCookie = decodeURIComponent(document.cookie);
    var ca = decodedCookie.split(';');
    for(var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') {
            c = c.substring(1);
        }
        if (c.indexOf(name) == 0) {
            return c.substring(name.length, c.length);
        }
    }
    return "";
}

// Do not allow multiple call center tabs
if (~window.location.hash.indexOf('#admin/callcenter')) {
    $(window).on('beforeunload onbeforeunload', function(){
        document.cookie = 'ic_window_id=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    });

    function validateCallCenterTab() {
        var win_id_cookie_duration = 10; // in seconds

        if (!window.name) {
            window.name = Math.random().toString();
        }

        if (!getCookie('ic_window_id') || window.name === getCookie('ic_window_id')) {
            // This means they are using just one tab. Set/clobber the cookie to prolong the tab's validity.
            setCookie('ic_window_id', window.name, win_id_cookie_duration);
        } else if (getCookie('ic_window_id') !== window.name) {
            // this means another browser tab is open, alert them to close the tabs until there is only one remaining
            var message = 'You cannot have this website open in multiple tabs. ' +
                'Please close them until there is only one remaining. Thanks!';
            $('html').html(message);
            clearInterval(callCenterInterval);
            throw 'Multiple call center tabs error. Program terminating.';
        }
    }

    callCenterInterval = setInterval(validateCallCenterTab, 3000);
}
