function your_block_name(id, config = {}) {
    const element = document.getElementById(id);

    /*
    construct your block here
    */

    function onEvent(data) {
        // handle data events given by the connect function
    }

    // return the onEvent function and the id
    return {
        onEvent: onEvent,
        id: id
    }
}