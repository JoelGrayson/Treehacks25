

// Generate random data for a single line
function generateData() {
    return Array.from({length: 10}, () => Math.floor(Math.random() * 401) - 200);
}

// Generate a random color
function getRandomColor() {
    const r = Math.floor(Math.random() * 256);
    const g = Math.floor(Math.random() * 256);
    const b = Math.floor(Math.random() * 256);
    return `rgb(${r}, ${g}, ${b})`;
}

// Create labels for the x-axis (time points)
const labels = Array.from({length: 10}, (_, i) => ``);
// const labels = Array.from({length: 10}, (_, i) => `T${i + 1}`);

// Create 16 charts
const chartsContainer = document.getElementById('chartsContainer');
let charts=[];

for (let i = 0; i < 16; i++) {
    const chartWrapper = document.createElement('div');
    chartWrapper.className = 'chart-wrapper';
    chartWrapper.innerHTML=`<h3 class='text-center font-bold'>EEG ${i+1}</h3>`;
    
    const canvas = document.createElement('canvas');
    chartWrapper.appendChild(canvas);
    chartsContainer.appendChild(chartWrapper);

    const ctx = canvas.getContext('2d');
    
    chart=new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: `Dataset ${i + 1}`,
                data: generateData(),
                borderColor: getRandomColor(),
                tension: 0.1,
                fill: false
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: false,
                    suggestedMin: -200,
                    suggestedMax: 200
                }
            },
            plugins: {
                legend: {
                    display: false
                }
            }
        }
    });
    charts.push(chart);
}




// Generate random data for a single line
function generateData() {
    return Array.from({length: 10}, () => Math.floor(Math.random() * 401) - 200);
}

// Generate a random color
function getRandomColor() {
    const r = Math.floor(Math.random() * 256);
    const g = Math.floor(Math.random() * 256);
    const b = Math.floor(Math.random() * 256);
    return `rgb(${r}, ${g}, ${b})`;
}
