const ctx = document.getElementById('expenseChart');

new Chart(ctx, {
    type: 'pie',
    data: {
        labels: [
            'Food',
            'Transport',
            'Bills',
            'Shopping'
        ],
        datasets: [{
            data: [5000,3000,2000,4000]
        }]
    }
});