document.addEventListener('DOMContentLoaded', function () {
    const ctx = document.getElementById('healthChart').getContext('2d');
    let healthChart;
    let currentChartType = 'line';

    const categoryFilter = document.getElementById('categoryFilter');
    const diseaseFilter = document.getElementById('diseaseFilter');
    const titleFilter = document.getElementById('titleFilter');
    const lineChartBtn = document.getElementById('lineChartBtn');
    const barChartBtn = document.getElementById('barChartBtn');
    const resetZoomBtn = document.getElementById('resetZoomBtn');

    function updateChart() {
        const categoryId = categoryFilter.value;
        const diseaseId = diseaseFilter.value;
        const selectedTitles = Array.from(titleFilter.selectedOptions).map(option => option.value);

        let url = `/health/chart-data/?category=${categoryId}&disease=${diseaseId}`;
        selectedTitles.forEach(title => {
            url += `&titles[]=${encodeURIComponent(title)}`;
        });

        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (healthChart) {
                    healthChart.destroy();
                }

                const existingTitles = new Set(Array.from(titleFilter.options).map(o => o.value));
                data.all_titles.forEach(title => {
                    if (!existingTitles.has(title)) {
                        const option = new Option(title, title, false, selectedTitles.includes(title));
                        titleFilter.add(option);
                    }
                });
                const instance = M.FormSelect.getInstance(titleFilter);
                instance.destroy();
                M.FormSelect.init(titleFilter);

                healthChart = new Chart(ctx, {
                    type: currentChartType,
                    data: {
                        labels: data.datasets.length > 0 ? data.datasets[0].dates : [],
                        datasets: data.datasets.map(ds => ({
                            label: ds.label,
                            data: ds.data,
                            borderColor: getRandomColor(),
                            backgroundColor: function(context) {
                                const index = context.dataIndex;
                                const outOfRange = ds.out_of_range[index];
                                return outOfRange ? 'rgba(255, 99, 132, 0.7)' : 'rgba(75, 192, 192, 0.5)';
                            },
                            borderWidth: 2,
                            fill: currentChartType === 'line' ? false : true,
                            tension: 0.1,
                            pointRadius: function(context) {
                                const index = context.dataIndex;
                                const outOfRange = ds.out_of_range[index];
                                return outOfRange ? 6 : 3;
                            },
                            pointBackgroundColor: function(context) {
                                const index = context.dataIndex;
                                const outOfRange = ds.out_of_range[index];
                                return outOfRange ? 'red' : 'blue';
                            }
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
                            tooltip: {
                                callbacks: {
                                    footer: function (tooltipItems) {
                                        let footer = '';
                                        tooltipItems.forEach(function (tooltipItem) {
                                            const dataset = data.datasets[tooltipItem.datasetIndex];
                                            const comment = dataset.comments[tooltipItem.dataIndex];
                                            if (comment) {
                                                footer += `Comment: ${comment}\n`;
                                            }
                                        });
                                        return footer;
                                    }
                                }
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
    titleFilter.addEventListener('change', updateChart);

    lineChartBtn.addEventListener('click', () => {
        currentChartType = 'line';
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
    M.FormSelect.init(titleFilter);

    updateChart();
});