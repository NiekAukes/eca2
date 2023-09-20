function barchart(id, config = {}) {
    const ctx = document.getElementById(id);
    const chart = new Chart(ctx, {
        type: 'bar',
        data: config.data || {
            labels: [],
            datasets: [{
                label: "Data",
                data: [],
                backgroundColor: [
                    "rgba(255, 99, 132, 0.6)",
                    "rgba(54, 162, 235, 0.6)",
                    "rgba(75, 192, 192, 0.6)"
                ],
                borderWidth: 1
            }]
        },
        options: config.options || {}
    });

    function onEvent(data) {
        // data = {action: "set/add/reset", value: [category: string, value: int]}
        if (data.action === "set") {
             // if the category doesn't exist, add it
            let category = data.value[0];
            if (!chart.data.labels.includes(category)) {
                chart.data.labels.push(category);
                chart.data.datasets[0].data.push(0);
            }
            // find the index of the category
            let index = chart.data.labels.indexOf(category);
            // set the value to the data
            chart.data.datasets[0].data[index] = data.value[1];
        }
        else if (data.action === "add") {
            // if the category doesn't exist, add it
            let category = data.value[0];
            if (!chart.data.labels.includes(category)) {
                chart.data.labels.push(category);
                chart.data.datasets[0].data.push(0);
            }
            // find the index of the category
            let index = chart.data.labels.indexOf(category);
            // add the value to the data
            chart.data.datasets[0].data[index] += data.value[1];
        }
        else if (data.action === "reset") {
            chart.data.datasets[0].data = [];
        } else {
            console.warn("Invalid action: " + data.action);
        }
        chart.update();
    }

    // return the onEvent function
    return onEvent;
}