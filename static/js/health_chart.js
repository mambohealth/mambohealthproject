document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('healthChart').getContext('2d');
    let healthChart;
    let currentChartType = 'line'; // Line chart is default

    const lineChartBtn = document.getElementById('lineChartBtn');
    const areaChartBtn = document.getElementById('areaChartBtn');
    const barChartBtn = document.getElementById('barChartBtn');
    const resetZoomBtn = document.getElementById('resetZoomBtn');

    function updateChart() {
        // Construct URL from current page's query parameters
        const url = new URL(window.location.href);
        url.pathname = '/health/chart-data/'; // Target the chart data endpoint
        
        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (healthChart) {
                    healthChart.destroy();
                }

                const chartContainer = document.getElementById('healthChart').parentElement;
                let noDataMsg = document.getElementById('no-data-message');
                if (!data.datasets || data.datasets.length === 0) {
                    if (!noDataMsg) {
                        noDataMsg = document.createElement('div');
                        noDataMsg.id = 'no-data-message';
                        noDataMsg.className = 'text-center text-gray-500 py-8';
                        noDataMsg.innerText = 'No data available for the selected filters.';
                        chartContainer.appendChild(noDataMsg);
                    }
                    return;
                } else {
                    if (noDataMsg) noDataMsg.remove();
                }

                // If out_of_range filter is active, filter out non-out-of-range points client-side as well
                const params = new URLSearchParams(window.location.search);
                const outOfRangeActive = params.get('out_of_range') === 'on';

                healthChart = new Chart(ctx, {
                    type: currentChartType === 'area' ? 'line' : currentChartType,
                    data: {
                        datasets: data.datasets.map((ds, i) => ({
                            label: ds.label,
                            data: outOfRangeActive ? ds.data.filter(d => d.out_of_range) : ds.data,
                            borderColor: `hsl(${i * 60}, 70%, 50%)`,
                            backgroundColor: currentChartType === 'area' ? `hsla(${i * 60}, 70%, 50%, 0.2)` : `hsla(${i * 60}, 70%, 50%, 0.5)`,
                            borderWidth: 2,
                            fill: currentChartType === 'area',
                            pointRadius: (context) => (context.raw && context.raw.out_of_range) ? 8 : 4,
                            pointStyle: (context) => (context.raw && context.raw.out_of_range) ? 'rectRot' : 'circle',
                            pointBackgroundColor: (context) => (context.raw && context.raw.out_of_range) ? '#ef4444' : `hsl(${i * 60}, 70%, 50%)`,
                        }))
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            x: {
                                type: 'time',
                                time: {
                                    unit: 'day',
                                    tooltipFormat: 'yyyy-MM-dd'
                                },
                                title: {
                                    display: true,
                                    text: 'Date'
                                }
                            },
                            y: {
                                title: {
                                    display: true,
                                    text: 'Value'
                                }
                            }
                        },
                        plugins: {
                            tooltip: {
                                enabled: true,
                                callbacks: {
                                    label: function(context) {
                                        const point = context.raw;
                                        const ds = context.dataset;
                                        let label = `${ds.label}: ${point.y}`;
                                        if (point.out_of_range) {
                                            label += ` (Out of Range)`;
                                        }
                                        return label;
                                    }
                                }
                            },
                            legend: {
                                display: true
                            }
                        }
                    }
                });
            })
            .catch(error => console.error('Error fetching or processing chart data:', error));
    }

    // Chart type buttons
    lineChartBtn.addEventListener('click', () => {
        currentChartType = 'line';
        updateChart();
    });
    areaChartBtn.addEventListener('click', () => {
        currentChartType = 'area';
        updateChart();
    });
    barChartBtn.addEventListener('click', () => {
        currentChartType = 'bar';
        updateChart();
    });
    resetZoomBtn.addEventListener('click', () => {
        if (healthChart) {
            healthChart.resetZoom();
        }
    });

    // Initial chart load
    updateChart();
});