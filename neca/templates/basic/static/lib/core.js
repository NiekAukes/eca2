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
    // check if block is callable
    if (typeof block !== "function") {
        console.log("Block is not callable");
        return;
    }

    // add listener that triggers events in DOM
    socket.on(key, function(message) {
        // trigger the event
        console.log("Triggering event: ", key);
        block(message);
    });
}
