function barChart() {
    const ctx = document.getElementById('myChart').getContext('2d');
    const labels = ['α', 'β', 'γ', 'δ', 'θ'];
    const initialData = [0, 0, 0, 0, 0];

    const chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                data: initialData,
                // hide label
                label: '',
                backgroundColor: [
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(54, 162, 235, 0.7)',
                    'rgba(255, 206, 86, 0.7)',
                    'rgba(75, 192, 192, 0.7)',
                    'rgba(153, 102, 255, 0.7)'
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            animation: {
                duration: 500
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100
                }
            }
        }
    });

    function updateChart() {
        const newData = chart.data.datasets[0].data.map(() => Math.floor(Math.random() * 100));
        chart.data.datasets[0].data = newData;
        chart.update();
    }

    // Update the chart every second
    setInterval(updateChart, 1000);
}

