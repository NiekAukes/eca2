function rolling_chart(id, config = {}) {

    const chart = new Chart(id, {
        type: 'line',
        data: {
            labels: config.labels || [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
            datasets: [{
                label: config.label || "Data",
                data: config.data || [],
                backgroundColor: config.backgroundColor || "rgba(255, 99, 132, 0.2)",
                borderColor: config.borderColor || "rgba(255, 99, 132, 1)",
                borderWidth: config.borderWidth || 1
            }]
        },
        options: {
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
            }
        }
    });

    function createSeries(series, values) {
        // create a new series
        chart.data.datasets.push({
            label: series,
            data: values,
            backgroundColor: config.backgroundColor || "rgba(255, 99, 132, 0.2)",
            borderColor: config.borderColor || "rgba(255, 99, 132, 1)",
            borderWidth: config.borderWidth || 1
        });
    }


    function onEvent(data) {
        // handle data events given by the connect function
        if (!data.action) {
            // user probably made a mistake,
            // log an error
            console.error("Invalid action: " + data.action);
            return;
        }

        if (data.action == "set") {
            // get the series
            let series = data.series || chart.data.datasets[0].label;

            // get the values, in the form: [[x1, x2], [y1, y2], ...]
            let values = data.values;


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
            // add a new value to the chart
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
                chart.data.datasets[index].data.push(value);
                
                // if the length of the series is greater than the amount of labels,
                // remove the first value
                if (chart.data.datasets[index].data.length > chart.data.labels.length) {
                    chart.data.datasets[index].data.shift();
                }
            }

            // update the chart
            chart.update();
        }

        else if (data.action == "reset") {
            // reset the chart
            chart.data.datasets = [{
                label: config.label || "Data",
                data: [],
                backgroundColor: config.backgroundColor || "rgba(255, 99, 132, 0.2)",
                borderColor: config.borderColor || "rgba(255, 99, 132, 1)",
                borderWidth: config.borderWidth || 1
            }];

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