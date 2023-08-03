function your_block_name(id, config = {}) {
    const element = document.getElementById(id);

    /*
    construct your block here
    */

    function onEvent(data) {
        // handle data events given by the connect function
    }

    // return the onEvent function and the id of the binding element
    return {
        onEvent: onEvent,
        id: id
    }
}