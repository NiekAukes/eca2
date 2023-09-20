function log_block(id, config = {}) {
    const element = document.getElementById(id);

    function onEvent(data) {
        // handle data events given by the connect function

        // add the message as a paragraph
        var p = document.createElement("p");
        p.innerHTML = data.message;
        if (!data.message) {
            p.innerHTML = "No message given";
        }
        element.appendChild(p);
    }

    // return the onEvent function and the id
    return onEvent;
}