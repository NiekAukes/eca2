function pie_chart(id, config = {}) {
    const ctx = document.getElementById(id);
    new Chart(ctx, {
        type: 'pie',
        data: config.data || {
            labels: [0, 1, 2],
            datasets: [{
                label: "Data",
                data: [1,2,3],
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
        // handle data events given by the connect function
    }

    // return the onEvent function and the id of the binding element
    return {
        onEvent: onEvent,
        id: id
    }
}