$(function () {


    // Submit post on submit
    $('#puzzle_form').on('submit', function (event) {
        event.preventDefault();
        console.log("form submitted!"); // sanity check
        puzzle_submit();
    });

    // AJAX for posting
    function puzzle_submit() {
        console.log("puzzle submit is working!"); // sanity check
        $.ajax({
            url: "submit_puzzle/{%pk%}", // the endpoint
            type: "POST", // http method
            data: {answer: $('#answer').val()}, // data sent with the post request
            // handle a successful response
            success: function (json) {
                $('#answer').val(''); // remove the value from the input
                console.log(json); // log the returned json to the console
                $("#next_button").prepend("<button id=\"next\" class=\"btn waves-effect waves-light\" type=\"submit\" style=\"margin-left: 100px\">\n" +
                    "            Next\n" +
                    "            <i class=\"material-icons right\">arrow_forward</i>\n" +
                    "        </button>");
                console.log("success"); // another sanity check
            },
            // handle a non-successful response
            error: function (xhr, errmsg, err) {
                $('#error').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: " + errmsg +
                    " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
                console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            }
        });
    };


    // This function gets cookie with a given name
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie != '') {
            let cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    let csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        let host = document.location.host; // host + port
        let protocol = document.location.protocol;
        let sr_origin = '//' + host;
        let origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});