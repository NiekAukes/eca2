// connect a websocket to the server

const SERVER_URL = "localhost:8080"
var socket = io();

// keep track of all blocks
// and their ids
var blocks = {};

socket.on('connect', function() {
    console.log("Connected to server");
});


// create new connections between blocks and events
// when the connect() function is called in the template

// connect("tweets", ".tweet")
// connect("graph", ".graph")

function connect_block(name, blockId) {
    //get the block element 
    try {
        var block = blocks[blockId];
    } catch(err) {
        console.log("Block not found: ", blockId);
        return;
    }

    // add listener that triggers events in DOM
    socket.on(name, function(message) {
        // trigger the event
        console.log("Triggering event: ", name);
        block(message);
    });
}


// create a block function that allows for quick creation of new block types.
// block("tweets", "#tweet").tweets()
// block("graph", "#graph").graph()
// block("xyz", "#xyz").xyz()


function add_block(block) {
    // declare a new block bound to the given id
    blocks[block.id] = block.onEvent;
    
    // TODO: do some other stuff we need to do 
    // to initialize the block
}