document.addEventListener('DOMContentLoaded', function () {
    // State variables
    let outOfRangeOnly = false;
    // Chart type is always 'line'
    let recordsByCategoryChartInstance = null;

   
    // Chart type selection removed; chart will always be line

    // Fetch KPI data
    fetch('/health/api/dashboard-kpi-data/')
        .then(response => response.json())
        .then(data => {
            document.getElementById('kpi-total-records').textContent = data.total_records_this_month;
            document.getElementById('kpi-avg-severity').textContent = data.average_symptom_severity;
            document.getElementById('kpi-med-adherence').textContent = `${data.medication_adherence_rate}%`;
        })
        .catch(error => {
            document.getElementById('kpi-total-records').textContent = 'Error';
            document.getElementById('kpi-avg-severity').textContent = 'Error';
            document.getElementById('kpi-med-adherence').textContent = 'Error';
            console.error('KPI fetch error:', error);
        });

    function getRandomColor() {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }

    function renderRecordsByCategoryChart(dataType = 'count', startDate = null, endDate = null, healthCategoryId = null, diseaseCategoryId = null) {
        let url = `/health/api/records-by-category-data/?data_type=${dataType}`;
        if (startDate) url += `&start_date=${startDate}`;
        if (endDate) url += `&end_date=${endDate}`;
        if (healthCategoryId) url += `&health_category_id=${healthCategoryId}`;
        if (diseaseCategoryId) url += `&disease_category_id=${diseaseCategoryId}`;

        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (recordsByCategoryChartInstance) {
                    recordsByCategoryChartInstance.destroy();
                }

                console.log('Raw data sample:', data);

                const ctx = document.getElementById('recordsByCategoryChart').getContext('2d');
                let datasets = [];

                if (dataType === 'individual') {
                    if (outOfRangeOnly) {
                        const filtered = data.filter(item => item.out_of_range === true);
                        console.log(`Filtered to ${filtered.length} out-of-range items out of ${data.length}`);
                        data = filtered;
                    }

                    const titleMap = new Map();
                    data.forEach(item => {
                        const title = item.title || 'Untitled';
                        if (!titleMap.has(title)) {
                            titleMap.set(title, {
                                label: title,
                                data: [],
                                borderColor: getRandomColor(),
                                backgroundColor: 'rgba(0,0,0,0)',
                                fill: false,
                                tension: 0.3,
                                pointBackgroundColor: [],
                                pointRadius: [],
                            });
                        }
                        const ds = titleMap.get(title);
                        ds.data.push({
                            x: item.date,
                            y: item.value,
                            comments: item.comments || '',
                            out_of_range: item.out_of_range,
                            normal_min: item.normal_min,
                            normal_max: item.normal_max,
                        });
                        ds.pointBackgroundColor.push(item.out_of_range ? 'red' : 'blue');
                        ds.pointRadius.push(item.out_of_range ? 6 : 3);
                    });

                    // Only include titles with data in legend
                    datasets = Array.from(titleMap.values())
                        .filter(ds => ds.data.length > 0)
                        .map(ds => ({
                            ...ds,
                            pointBackgroundColor: ds.pointBackgroundColor,
                            pointRadius: ds.pointRadius,
                        }));

                } else {
                    const categoryMap = new Map();
                    data.forEach(item => {
                        const cat = item.category__name || 'Uncategorized';
                        if (!categoryMap.has(cat)) {
                            categoryMap.set(cat, {
                                label: cat,
                                data: [],
                                borderColor: getRandomColor(),
                                backgroundColor: 'rgba(0,0,0,0)',
                                fill: false,
                                tension: 0.3
                            });
                        }
                        categoryMap.get(cat).data.push({
                            x: item.date,
                            y: item.value
                        });
                    });
                    datasets = Array.from(categoryMap.values());
                }

                recordsByCategoryChartInstance = new Chart(ctx, {
                    type: 'line',
                    data: { datasets },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        scales: {
                            x: {
                                type: 'time',
                                time: { unit: 'day', tooltipFormat: 'PP' },
                                title: { display: true, text: 'Date' }
                            },
                            y: {
                                beginAtZero: true,
                                title: { display: true, text: 'Value' }
                            }
                        },
                        plugins: {
                            legend: { display: true },
                            tooltip: {
                                callbacks: {
                                    label: function(context) {
                                        let label = context.dataset.label || '';
                                        if (label) label += ': ';
                                        if (context.parsed.y !== null) label += context.parsed.y;
                                        if (context.raw?.x) label += ` | Date: ${context.raw.x}`;
                                        if (context.raw?.comments) label += ` | Comments: ${context.raw.comments}`;
                                        if (context.raw?.out_of_range) label += ' (Out of Range)';
                                        if (context.raw?.normal_min || context.raw?.normal_max) {
                                            label += ` | Normal Range: ${context.raw.normal_min ?? '-'} - ${context.raw.normal_max ?? '-'}`;
                                        }
                                        return label;
                                    }
                                }
                            },
                            zoom: {
                                pan: { enabled: true, mode: 'xy' },
                                zoom: { wheel: { enabled: true }, pinch: { enabled: true }, mode: 'xy' }
                            }
                        },
                        elements: {
                            point: {
                                backgroundColor: ctx => ctx.dataset.pointBackgroundColor?.[ctx.dataIndex] || 'blue',
                                radius: ctx => ctx.dataset.pointRadius?.[ctx.dataIndex] || 3
                            }
                        }
                    }
                });
            });
    }

    function updateRecordsByCategoryChart() {
        const selectedType = document.querySelector('input[name="records_by_category_type"]:checked')?.value || 'count';
        const startDate = document.getElementById('recordsByCategoryStartDate')?.value || null;
        const endDate = document.getElementById('recordsByCategoryEndDate')?.value || null;
        const healthCategoryId = document.getElementById('healthCategoryFilter')?.value || null;
        const diseaseCategoryId = document.getElementById('diseaseCategoryFilter')?.value || null;

        renderRecordsByCategoryChart(selectedType, startDate, endDate, healthCategoryId, diseaseCategoryId);
    }

    // Initial chart render
    renderRecordsByCategoryChart();

    // Use the out-of-range checkbox from the template
    document.getElementById('outOfRangeOnlyToggle')?.addEventListener('change', function(e) {
        outOfRangeOnly = e.target.checked;
        updateRecordsByCategoryChart();
    });

    // Type filter
    document.querySelectorAll('input[name="records_by_category_type"]').forEach(radio => {
        radio.addEventListener('change', updateRecordsByCategoryChart);
    });

    // Date buttons
    document.querySelectorAll('.chart-panel button[data-days]').forEach(button => {
        button.addEventListener('click', (e) => {
            const days = parseInt(e.target.dataset.days);
            const today = new Date();
            const startDate = new Date(today);
            startDate.setDate(today.getDate() - days);

            document.getElementById('recordsByCategoryStartDate').value = startDate.toISOString().split('T')[0];
            document.getElementById('recordsByCategoryEndDate').value = today.toISOString().split('T')[0];

            updateRecordsByCategoryChart();
        });
    });

    // Apply Date button
    document.getElementById('recordsByCategoryApplyDate')?.addEventListener('click', updateRecordsByCategoryChart);

    // Filter dropdowns
    document.getElementById('healthCategoryFilter')?.addEventListener('change', updateRecordsByCategoryChart);
    document.getElementById('diseaseCategoryFilter')?.addEventListener('change', updateRecordsByCategoryChart);
});
