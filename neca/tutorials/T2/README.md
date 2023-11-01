# Tutorial 2: Creating your first Block
in this tutorial, we will create a simple rolling graph that displays a moving sine wave. we will use the `emit()` function to keep the graph updated.

## Learning goals
- Learn about pages in neca and flask
- Learn about blocks inside pages
- Learn how to connect blocks to your python code
- Learn about the `emit()` function

## Pages
in neca, your main HTML page is located in `templates/index.html`. this is the page that will be displayed when you run your project. you can also add more pages, see the wiki entry on [pages](https://github.com/NiekAukes/eca2/wiki/Server-documentation#extending-your-web-server-with-flask)

## Blocks
NECA uses blocks to display graphs and other visuals on your web page. There are multiple Block types available, all with their own .js file in the `static/lib` folder. Each block type has its own set of parameters, which can be found in the wiki entry on [blocks](https://github.com/NiekAukes/eca2/wiki/Blocks).

### Task 1: Create a line_chart block
create a line chart block on your page. you can use the wiki page on [line charts](line-chart) to find out how to do this. make sure to give it a unique id, for example `my_chart`.

<details>
<summary>Hint 1 (HTML)</summary>

create a new `<div>` element with inside it a `<canvas>` element. give the `<canvas>` element an id, for example `my_chart`.

```html
<div>
    <canvas id="my_chart"></canvas>
</div>
```
</details>

<details>
<summary>Hint 2 (JS)</summary>

create a new `line_chart` block with the id you gave the `<canvas>` element.

```js
let my_chart_handler = linechart("my_chart");
```

</details>

<details>
<summary>Solution</summary>

```html
<div>
    <canvas id="my_chart"></canvas>
</div>
<script>
    var my_chart_handler = linechart("my_chart");
</script>
```
</details>

## Connecting blocks to your python code
to connect blocks to your python code, you need to use the `connect_block()` function. This function takes 2 arguments, first the block itself, and second the key that will be used to identify the data that is sent to the block. the key can be any string, but it is recommended to use a descriptive name. for example, if you are sending data about the temperature, you could use `temperature` as the key.
```html
<script>
    let my_chart_handler = linechart("my_chart");
    connect_block(my_chart_handler, "temperature");
</script>
```

### Task 2: Connect the line_chart block to your python code

connect the line_chart block to your python code using the `connect_block()` function. use the key `sine`.

<details>
<summary>Solution</summary>
    
```html
<script>
    let my_chart_handler = linechart("my_chart");
    connect_block(my_chart_handler, "sine");
</script>
```
</details>

## The `emit()` function
the `emit()` function is used to send data to the web page. it takes two arguments: a key and some data. the key is used to identify the data, much like how events are identified by their name. the data can be any python object, but specific blocks may require specific types of data. for example, the `log` block requires a string, while the `graph` block requires a dictionary with a specific structure.
```python
from neca.events import emit
emit("key", "data")
```

### Task 3: Emit some data
use the `emit()` function to send some data to the web page. use the key `sine` and send 2 values:
```python
{
    "action": "add",
    "value": [0,0]
}
# and
{
    "action": "add",
    "value": [1,1]
}
```

<details>
<summary>Solution</summary>

```python
@event("init")
def init():
    emit("sine", {
        "action": "add",
        "value": [0,0]
    })
    emit("sine", {
        "action": "add",
        "value": [1,1]
    })
```
</details>


### Task 4: Emit a sine wave
create a perpetual loop that emits a sine wave. you can use the `math.sin()` function to calculate the sine of a value. you may set a frequency of 100ms per update.

<details>
<summary>Hint 1</summary>

you can repeatedly fire the same event every 0.1 by using 
```python
fire_global("sinewave", ?, delay=0.1)
```
this will fire the event `sinewave` every 0.1 seconds. you can use this to create a perpetual loop.
</details>

<details>
<summary>Hint 2</summary>

use the data parameter to define your x value for the sine wave. you can use the `math.sin()` function to calculate the y value.

```python
@event("sinewave")
def sine(context, data):
    # other code  
    x = data
    # other code

    fire_global("sinewave", x+0.1, delay=0.1)  
```

</details>

<details>
<summary>Solution</summary>

```python
@event("init")
def init(context, data):
    fire_global("sinewave", 0)

@event("sinewave")
def sine(context, data):
    x = data
    y = math.sin(x)
    emit("sine", {
        "action": "add",
        "value": [x,y]
    })
    fire_global("sinewave", x+0.1, delay=0.1)
```
</details>