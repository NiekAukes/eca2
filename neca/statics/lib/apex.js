function apexchart(id, config = {}) {
    const element = document.getElementById(id);

    let chart = new ApexCharts(element, config);
    chart.render();
    chart.onEvent = function (data) {
        if (data.action === "updateSeries") {
            chart.updateSeries(data.newSeries, data.animate);
        }
        else if (data.action === "updateOptions") {
            chart.updateOptions(data.newOptions, data.redrawPaths, data.animate, data.updateSyncedCharts);
        }
        else if (data.action === "appendSeries") {
            chart.appendSeries(data.newSeries, data.animate);
        }
        else if (data.action === "appendData") {
            chart.appendData(data.newData);
        }
        else {
            console.warn("Invalid action: " + data.action);
        }
    }

    return chart;
}