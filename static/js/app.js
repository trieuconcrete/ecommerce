var message_timer = document.getElementById("message-timer");

setTimeout(function() {

    if (message_timer && message_timer.style) {
        message_timer.style.display = "none";
    }

} ,2500)