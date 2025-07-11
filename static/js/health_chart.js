document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('healthChart').getContext('2d');
    let healthChart;
    let currentChartType = 'line';

    const categoryFilter = document.getElementById('categoryFilter');
    const diseaseFilter = document.getElementById('diseaseFilter');
    const lineChartBtn = document.getElementById('lineChartBtn');
    const areaChartBtn = document.getElementById('areaChartBtn');
    const barChartBtn = document.getElementById('barChartBtn');
    const resetZoomBtn = document.getElementById('resetZoomBtn');

    function updateChart() {
        const categoryId = categoryFilter.value;
        const diseaseId = diseaseFilter.value;
        let url = `/health/chart-data/?category=${categoryId}&disease=${diseaseId}`;
        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (healthChart) {
                    healthChart.destroy();
                }
                // Show "No data available" message if no datasets
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

                // Prepare annotation plugin config for healthy ranges
                let annotations = {};
                data.datasets.forEach((ds, i) => {
                    if (ds.normal_min !== null && ds.normal_min !== '' && !isNaN(ds.normal_min)) {
                        annotations[`min${i}`] = {
                            type: 'line',
                            yMin: parseFloat(ds.normal_min),
                            yMax: parseFloat(ds.normal_min),
                            borderColor: 'rgba(34,197,94,0.7)',
                            borderWidth: 2,
                            label: {
                                display: true,
                                content: 'Min',
                                position: 'start',
                                color: 'rgba(34,197,94,0.7)',
                            }
                        };
                    }
                    if (ds.normal_max !== null && ds.normal_max !== '' && !isNaN(ds.normal_max)) {
                        annotations[`max${i}`] = {
                            type: 'line',
                            yMin: parseFloat(ds.normal_max),
                            yMax: parseFloat(ds.normal_max),
                            borderColor: 'rgba(34,197,94,0.7)',
                            borderWidth: 2,
                            label: {
                                display: true,
                                content: 'Max',
                                position: 'end',
                                color: 'rgba(34,197,94,0.7)',
                            }
                        };
                    }
                });

                healthChart = new Chart(ctx, {
                    type: currentChartType === 'area' ? 'line' : currentChartType,
                    data: {
                        labels: data.datasets.length > 0 ? data.datasets[0].dates : [],
                        datasets: data.datasets.map((ds, i) => ({
                            label: ds.label,
                            data: ds.data,
                            borderColor: `hsl(${i * 60}, 70%, 50%)`,
                            backgroundColor: currentChartType === 'area' ? `hsla(${i * 60}, 70%, 50%, 0.2)` : 'rgba(75, 192, 192, 0.5)',
                            borderWidth: 2,
                            fill: currentChartType === 'area',
                            tension: 0.3,
                            pointRadius: ds.out_of_range.map(v => v ? 8 : 4),
                            pointStyle: ds.out_of_range.map(v => v ? 'rectRot' : 'circle'),
                            pointBackgroundColor: ds.out_of_range.map(v => v ? '#ef4444' : `hsl(${i * 60}, 70%, 50%)`),
                        }))
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            x: {
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
                            legend: {
                                display: true,
                                onClick: function(e, legendItem, legend) {
                                    const label = legendItem.text;
                                    const meta = healthChart.getDatasetMeta(legendItem.datasetIndex);
                                    meta.hidden = meta.hidden === null ? !healthChart.data.datasets[legendItem.datasetIndex].hidden : null;
                                    healthChart.update();
                                }
                            },
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        const ds = data.datasets[context.datasetIndex];
                                        const idx = context.dataIndex;
                                        let label = `${ds.label}: ${context.parsed.y}`;
                                        label += `\nDate: ${context.parsed.x}`;
                                        if (ds.normal_min !== null && ds.normal_min !== '' && !isNaN(ds.normal_min)) {
                                            label += `\nHealthy Min: ${ds.normal_min}`;
                                        }
                                        if (ds.normal_max !== null && ds.normal_max !== '' && !isNaN(ds.normal_max)) {
                                            label += `\nHealthy Max: ${ds.normal_max}`;
                                        }
                                        if (ds.comments && ds.comments[idx]) label += `\nComment: ${ds.comments[idx]}`;
                                        if (ds.out_of_range[idx]) label += `\n⚠️ Out of Range`;
                                        return label;
                                    },
                                },
                            },
                            annotation: {
                                annotations: annotations
                            },
                            zoom: {
                                pan: {
                                    enabled: true,
                                    mode: 'x',
                                },
                                zoom: {
                                    wheel: {
                                        enabled: true,
                                    },
                                    pinch: {
                                        enabled: true
                                    },
                                    mode: 'x',
                                }
                            }
                        }
                    }
                });
            });
    }

    function getRandomColor() {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    categoryFilter.addEventListener('change', updateChart);
    diseaseFilter.addEventListener('change', updateChart);

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

    M.FormSelect.init(categoryFilter);
    M.FormSelect.init(diseaseFilter);

    updateChart();
});