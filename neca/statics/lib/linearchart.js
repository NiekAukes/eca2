function linearchart(id, config = {}) {

    // copy config.data to default_data
    const default_data = JSON.parse(JSON.stringify(config.data));

    // if config.options.showLine is not defined, set it to true
    if (config.options && config.options.showLine == undefined) {
        config.options.showLine = true;
    }

    const chart = new Chart(id, {
        type: 'scatter',
        data: config.data || {
            datasets: [{
                label:"Data",
                data: [[1,2],[2,1]],
                backgroundColor: "rgba(255, 99, 132, 0.2)",
                borderColor: "rgba(255, 99, 132, 1)",
                borderWidth: 1
            }]
        },
        options: config.options || {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Chart.js'
                }
            },
            scales: {
                x: {
                    display: true
                },
                y: {
                    display: true
                }
            },
            showLine: true
        }
    });

    function createSeries(series, values) {
        // create a new series
        chart.data.datasets.push({
            label: series,
            data: values
        });
    }


    function onEvent(data) {
        // handle data events given by the connect function
        if (!data.action) {
            // user probably made a mistake,
            // log an error
            console.error("No action given");
            return;
        }
        if (data.action == "data") {
            // replace the entire data with the new data
            chart.data = data.value;
            // update the chart
            chart.update();
        }
        else if (data.action == "set") {
            // set the entire dataset of the series
            // get the series
            let series = data.series || chart.data.datasets[0].label;

            // get the values, in the form: [[x1, x2], [y1, y2], ...]
            let values = data.value;


            // get the index of the series
            let index = chart.data.datasets.findIndex((dataset) => {
                return dataset.label == series;
            });

            // if the series doesn't exist, create it
            if (index == -1) {
                createSeries(series, values);
            } else {
                // otherwise, set the values
                chart.data.datasets[index].data = values;
            }

            // update the chart
            chart.update();
        }

        else if (data.action == "add") {
            // add a new value to the dataset of the series
            let value = data.value;
            let series = data.series || chart.data.datasets[0].label;

            // get the index of the series
            let index = chart.data.datasets.findIndex((dataset) => {
                return dataset.label == series;
            });


            // if the series doesn't exist, create it
            if (index == -1) {
                createSeries(series, [value]);
            } else {
                // otherwise, add the value
                let dataset = chart.data.datasets[index]
                dataset.data.push(value);
                
                // if the length of the series is greater than the memory,
                // remove the first value
                // only do this if the memory is defined
                if (dataset.memory && dataset.data.length > dataset.memory) {
                    dataset.data.shift();
                }
            }

            // update the chart
            chart.update();
        }

        else if (data.action == "reset") {
            // reset the chart
            chart.data = default_data || {
                labels: [],
                datasets: [{
                    label:"Data",
                    data: [],
                    backgroundColor: "rgba(255, 99, 132, 0.2)",
                    borderColor: "rgba(255, 99, 132, 1)",
                    borderWidth: 1
                }]
            };
            // update the chart
            chart.update();
        } else {
            // user probably made a mistake,
            // log an error
            console.error("Invalid action: " + data.action);
            return;
        }

    }

    // return the onEvent function and the id
    return onEvent;
}