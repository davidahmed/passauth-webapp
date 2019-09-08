"use strict";

var mouseMovements = new Array();
var usernameFieldLogs;
var passwordFieldLogs;
var mouseMeta;

var usernameField;
var passwordField;
var printLogs;
var passwordValue="";

document.onmousemove = handleMouseMove;

var hashCode = function(s){
    return s.split("").reduce(function(a,b){a=((a<<5)-a)+b.charCodeAt(0);return a&a},0);
}

function handleMouseMove(event)
{
    var dot, eventDoc, doc, body, pageX, pageY;
    event = event || window.event; // IE-ism
    // If pageX/Y aren't available and clientX/Y
    // are, calculate pageX/Y - logic taken from jQuery
        // Calculate pageX/Y if missing and clientX/Y available
    if (event.pageX == null && event.clientX != null) {
        eventDoc = (event.target && event.target.ownerDocument) || document;
        doc = eventDoc.documentElement;
        body = eventDoc.body;
        event.pageX = event.clientX +
          (doc && doc.scrollLeft || body && body.scrollLeft || 0) -
          (doc && doc.clientLeft || body && body.clientLeft || 0);
        event.pageY = event.clientY +
    (doc && doc.scrollTop  || body && body.scrollTop  || 0) -
    (doc && doc.clientTop  || body && body.clientTop  || 0 );
    }
    //mouseMovements.push([event.pageX, event.pageY, event.timeStamp])
    mouseMovements.push([event.pageX, event.pageY, $.now()])
}

function attachDurationHandler(element, arr){
    var totalTime = {};
    var pressed = {};

    element.onkeydown = function(e) {
        if (e.which in pressed) return;
        pressed[e.which] = $.now();
    };
    element.onkeyup = function(e) {

        if (!(e.which in pressed)){return;}

        var duration = $.now() - pressed[e.which];

        if (!(e.which in totalTime)) totalTime[e.which] = 0;
        totalTime[e.which] += duration;
        //console.log('Key ' + e.which + ' pressed for ' + duration);
        arr.push({'code': e.which, 'timestamp': pressed[e.which], 'duration': duration})
        delete pressed[e.which];
    };
};




window.onload = () => {
    usernameFieldLogs = new Array();
    passwordFieldLogs = new Array();
    mouseMeta = new Array();
    usernameField = document.getElementById('inputUsername');
    passwordField = document.getElementById('inputPassword');

    attachDurationHandler(document.getElementById('inputUsername'), usernameFieldLogs);
    attachDurationHandler(document.getElementById('inputPassword'), passwordFieldLogs);

    $('#submitButton').click(function(){
        if ($('input[name=clicked]').length == 0){
            $('#login-form').append($("<input>").attr("type", "hidden").attr("name","clicked").val("true"));
        }
    });

    $('#inputUsername').mousedown(function(e){
        mouseMeta.push(['mousedown', 'inputUsername', e.pageX, $(this).offset().left, e.pageY, $(this).offset().top, $.now()]);
        $('#inputUsername').off('mousedown');
    });

    $('#inputUsername').mouseup(function(e){
        mouseMeta.push(['mouseup', 'inputUsername', e.pageX, $(this).offset().left, e.pageY, $(this).offset().top, $.now()]);
        $('#inputUsername').off('mouseup');
    });

    $('#inputUsername').mouseenter(function(e){
        mouseMeta.push(['mouseenter', 'inputUsername', e.pageX, $(this).offset().left, e.pageY, $(this).offset().top, $.now()]);
        $('#inputUsername').off('mouseenter');
    });


    $('#inputPassword').mousedown(function(e){
        mouseMeta.push(['mousedown', 'inputPassword', e.pageX, $(this).offset().left, e.pageY, $(this).offset().top, $.now()]);
        $('#inputPassword').off('mousedown');
    });

    $('#inputPassword').mouseup(function(e){
        mouseMeta.push(['mouseup', 'inputPassword', e.pageX, $(this).offset().left, e.pageY, $(this).offset().top, $.now()]);
        $('#inputPassword').off('mouseup');
    });

    $('#inputPassword').mouseenter(function(e){
        mouseMeta.push(['mouseenter', 'inputPassword', e.pageX, $(this).offset().left, e.pageY, $(this).offset().top, $.now()]);
        $('#inputPassword').off('mouseenter');
    });

    $('#submitButton').mousedown(function(e){
        mouseMeta.push(['mousedown', 'submitButton', e.pageX, $(this).offset().left, e.pageY, $(this).offset().top, $.now()]);
        $('#submitButton').off('mousedown');
    });

    $('#submitButton').mouseup(function(e){
        mouseMeta.push(['mouseup', 'submitButton', e.pageX, $(this).offset().left, e.pageY, $(this).offset().top, $.now()]);
        $('#submitButton').off('mouseup');
    });

    $('#submitButton').mouseenter(function(e){
        mouseMeta.push(['mouseenter', 'submitButton', e.pageX, $(this).offset().left, e.pageY, $(this).offset().top, $.now()]);
        $('#submitButton').off('mouseenter');
    });



    $('#login-form').on('keyup keypress', function(e) {
      var keyCode = e.keyCode || e.which;
      if (keyCode === 13) {
        e.preventDefault();
        return false;
      }
    });

    $('#inputPassword').keydown(function(){
        $(this).attr('type', 'password');
    });

    $('#login-form').submit(function(e){
        e.preventDefault();
        printLogs();
        this.submit();
        $('input[name=clicked]').remove();
    });
};

var printLogs = function() {
    var passwordValue = $('#inputPassword').val();
    $('#login-form').append($("<input>").attr("type","hidden").attr("name","passwordValue").val(passwordValue));
    $('#login-form').append($("<input>").attr("type","hidden").attr("name","usernameLogs").val(JSON.stringify(usernameFieldLogs)));
    $('#login-form').append($("<input>").attr("type","hidden").attr("name","passwordLogs").val(JSON.stringify(passwordFieldLogs)));
    $('#login-form').append($("<input>").attr("type","hidden").attr("name","mouseLogs").val(JSON.stringify(mouseMovements)));
    $('#login-form').append($("<input>").attr("type","hidden").attr("name","mouseMeta").val(JSON.stringify(mouseMeta)));

    $('#inputPassword').attr('type', 'text').val("");

};

var signUp = function() {
    var passwordValue = $('#inputPassword').val();
    $('#login-form').append($("<input>").attr("type","hidden").attr("name","passwordValue").val(passwordValue));
    $('#login-form').append($("<input>").attr("type","hidden").attr("name","usernameLogs").val(JSON.stringify(usernameFieldLogs)));
    $('#login-form').append($("<input>").attr("type","hidden").attr("name","passwordLogs").val(JSON.stringify(passwordFieldLogs)));
    $('#login-form').append($("<input>").attr("type","hidden").attr("name","mouseLogs").val(JSON.stringify(mouseMovements)));
    $('#inputPassword').attr('type', 'text').val("");

};