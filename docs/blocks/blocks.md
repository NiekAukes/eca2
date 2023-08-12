# Blocks
in this section we will discuss about blocks and how to use them in your project. blocks are used to create a dynamic user interface for your project. they can be used to display data, receive input from the user or the server. 

## Types of blocks
currently, there are 6 types of blocks:
- [log](log.md), displays a logger
- [form](form.md), displays a form for the user to fill
- [linearchart](linear_chart.md), displays a linear x-y line chart
- [linechart](line_chart.md), displays a categorical line chart
- [barchart](bar_chart.md), displays a bar chart
- [piechart](pie_chart.md), displays a pie chart


each block has its own properties and methods. see their respective sections for more information.

you can also create your own custom blocks. see the [custom blocks](#custom-blocks) section for more information.

## Creating a block
to create a block, you first need to add the necessary imports depending on which block you want to create. These are described in the sections dedicated to each block. In our example, we will create a `line_chart` block.
```html
<head>
    <script src="/static/lib/linechart.js">
</head>
```

then, you need to create an element for the block. How to do this is described in the sections dedicated to each block. In our example, we will create a `canvas` element with an id of `my_chart`, which we will put inside a div for more control over the shape of the chart.
```html
<div class="chart">
    <canvas id="my_chart"></canvas>
</div>
```

finally, you need to create a block object in javascript, and connect it to a key.
```html
<script>
    var chart = line_chart('my_chart');
    connect_block(chart, 'wins');
</script>
```

## Updating data in a block
you can now update the data in the block from you python backend using the `emit()` function in `neca.events`. this function takes 2 arguments: the key of the block and the data to send to the block.
```python
from neca.events import emit

emit('wins', {'action': 'add', 'value': [10,10]})
```

## Configuring a block
you can configure a block by passing a config object to the block constructor. this object contains the configuration options for the block. see the sections dedicated to each block for more information about the configuration options.

## Custom blocks
to add a custom block, duplicate the `static/lib/new_block.js` file and rename it to the name of your block. Also rename the function inside the file to the name of your block. the content of the file should look like this:
```js
function your_block_name(id, config = {}) {
    const element = document.getElementById(id);

    /*
    construct your block here
    */

    function onEvent(data) {
        // handle data events given by the server part of your application
    }

    // return the onEvent function and the id
    return onEvent;
}
```

the first section of the function is you constructor
```js	
const element = document.getElementById(id);
/*
construct your block here
*/
```
this is where you construct your block. you can use the `element` variable to access the DOM element of the block. use this to add sub-elements to the block, such as buttons, text, styles, etc.

the second section of the function is the event handler
```js
function onEvent(data) {
    // handle data events given by the server part of your application
}
```
this function is called when the server sends data to the block. you can use this function to update the block with the new data.

finally, you need to return the event handler function of the block, with which you can connect the block to a key.
```js
return onEvent; // do not change this
```