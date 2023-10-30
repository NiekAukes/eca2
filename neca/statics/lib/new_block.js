function your_block_name(id, config = {}) {
    const element = document.getElementById(id);

    /*
    construct your block here
    */

    function onEvent(data) {
        // handle data events given by the server part of your application
    }

    // return the onEvent function
    return onEvent;
}