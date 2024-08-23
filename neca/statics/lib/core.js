// connect a websocket to the server

const SERVER_URL = "localhost:8080"
var socket = io();

socket.on('connect', function() {
    console.log("Connected to server");
});


// create new connections between blocks and events
// when the connect() function is called in the template

// connect("tweets", ".tweet")
// connect("graph", ".graph")

function connect_block(block, key) {
    // check if block is callable or has a function called onEvent
    if (typeof block === "object" && typeof block.onEvent === "function") {
        // add listener that triggers events in DOM
        socket.on(key, function(message) {
            // trigger the event
            console.log("Triggering event: ", key);
            block.onEvent(message);
        });
    }
    else if (typeof block === "function") {
        // add listener that triggers events in DOM
        socket.on(key, function(message) {
            // trigger the event
            console.log("Triggering event: ", key);
            block(message);
        });
    } else {
        console.log("Block is not callable");
    }

    
}
