# Pie chart block
## Description
This block is used to display data in a pie chart. useful for proportional data.
## Requirements
This block requires the following libraries:
- chart.js
- piechart.js

```html	
<script src="/static/lib/chart.js"></script>
<script src="/static/lib/piechart.js"></script>
```

## Configuration
```js
{
    data: {...}
    options: {...}
}
```

`data`: the data to display in the chart, in the format specified by [chart.js](https://www.chartjs.org/docs/latest/charts/doughnut.html)

`options`: the options to use for the chart, in the format specified by [chart.js](https://www.chartjs.org/docs/latest/charts/doughnut.html#dataset-properties).

## Actions
### set
```python
{
    "action": "set",
    "series": "series_name", # optional
    "value": [category, value]
}
```

sets the value for a specific category. If no series is specified, the data will be set for the first series.

### add
```python
{
    "action": "add",
    "series": "series_name", # optional
    "value": [category, value]
}
```

Adds the value to the current value for a specific category. If no series is specified, the data will be added for the first series.

### reset
```python
{
    "action": "reset",
    "series": "series_name" # optional
}
```

Resets the data for the specified series to the initial value specified in the data config (if given). If no series is specified, the data will be reset for all series.

## Example
This example is also available as a demo
```html
<div style="height: 400px; overflow hidden">
    <canvas id="myChart"></canvas>
</div>

<script>
    let chart = piechart('myChart', {
        data: {
            labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
            datasets: [{
                label: 'My First Dataset',
                data: [12, 19, 3, 5, 2, 3],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(153, 102, 255, 0.2)',
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)',
                    'rgba(255, 159, 64, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
        }
    });
    
    connect_block(chart, 'piechart')
</script>
```

```
emit("piechart", {
    "action": "set",
    "value": ["Red", 10]
})

emit("piechart", {
    "action": "add",
    "value": ["Blue", 20]
})
```


### Result
![output](../img/piechart.png)
![update](../img/piechart_update.png)