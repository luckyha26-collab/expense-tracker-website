const API_URL = 'http://127.0.0.1:5000/api';
let allExpenses = [];

// 1. Initialize the app
document.addEventListener('DOMContentLoaded', () => {
    loadExpenses();
    setupEventListeners();
});

function setupEventListeners() {
    const form = document.getElementById('expenseForm');
    if (form) {
        form.addEventListener('submit', handleFormSubmit);
    }
}

// 2. Load and Refresh Data
async function loadExpenses() {
    try {
        const response = await fetch(`${API_URL}/expenses`);
        if (!response.ok) throw new Error('Failed to fetch');
        
        const data = await response.json();
        // The backend returns a list, so we assign it directly
        allExpenses = Array.isArray(data) ? data : [];
        
        renderUI();
    } catch (error) {
        console.error('Error loading expenses:', error);
    }
}

// 3. Handle adding an expense
async function handleFormSubmit(e) {
    e.preventDefault();

    const expenseData = {
        amount: parseFloat(document.getElementById('amount').value),
        category: document.getElementById('category').value,
        description: document.getElementById('description').value,
        date: document.getElementById('date').value
    };

    try {
        const response = await fetch(`${API_URL}/expenses`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(expenseData)
        });

        if (response.ok) {
            e.target.reset(); // Clear the form
            await loadExpenses(); // Refresh the list
            alert('Expense added successfully!');
        }
    } catch (error) {
        console.error('Error adding expense:', error);
    }
}

// 4. Update the Screen (Table, Stats, Charts)
function renderUI() {
    const tbody = document.getElementById('expensesBody');
    const noExpenses = document.getElementById('noExpenses');

    if (!allExpenses || allExpenses.length === 0) {
        tbody.innerHTML = '';
        noExpenses.style.display = 'block';
        return;
    }

    noExpenses.style.display = 'none';
    
    // Fill the Table
    tbody.innerHTML = allExpenses.map(exp => `
        <tr>
            <td>${exp.date}</td>
            <td>${exp.category}</td>
            <td>${exp.description || '-'}</td>
            <td>$${parseFloat(exp.amount).toFixed(2)}</td>
            <td>
                <button class="btn btn-danger" onclick="deleteExpense('${exp._id}')">Delete</button>
            </td>
        </tr>
    `).join('');

    // Update Stats and Charts
    const stats = calculateStatistics(allExpenses);
    document.getElementById('totalExpenses').textContent = `$${stats.total.toFixed(2)}`;
    document.getElementById('expenseCount').textContent = stats.count;
    document.getElementById('avgExpense').textContent = `$${stats.average.toFixed(2)}`;

    updateCharts(allExpenses);
}

// 5. Logic for Statistics
function calculateStatistics(expenses) {
    const total = expenses.reduce((sum, exp) => sum + parseFloat(exp.amount || 0), 0);
    const count = expenses.length;
    return {
        total,
        count,
        average: count > 0 ? total / count : 0
    };
}

// 6. Logic for Charts
function updateCharts(expenses) {
    if (!expenses || expenses.length === 0) return;

    // Grouping data by date for a cleaner chart
    const labels = expenses.map(e => e.date);
    const values = expenses.map(e => e.amount);
    
    renderChart({ labels, values });
}

// 6.1 The Actual Chart Rendering Logic
function renderChart(data) {
    const canvas = document.getElementById('expenseChart');
    if (!canvas) {
        console.error("Canvas element 'expenseChart' not found in HTML!");
        return;
    }

    const ctx = canvas.getContext('2d');

    // IMPORTANT: Destroy the previous chart instance if it exists
    // This fixes the "flickering" bug when updating data
    if (window.myExpenseChart instanceof Chart) {
        window.myExpenseChart.destroy();
    }

    // Create a new Chart instance
    window.myExpenseChart = new Chart(ctx, {
        type: 'bar', // You can change this to 'line' or 'pie'
        data: {
            labels: data.labels,
            datasets: [{
                label: 'Expenses ($)',
                data: data.values,
                backgroundColor: 'rgba(102, 126, 234, 0.6)',
                borderColor: 'rgba(102, 126, 234, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}
// 7. Delete Expense
async function deleteExpense(id) {
    if (!confirm('Are you sure?')) return;
    try {
        const response = await fetch(`${API_URL}/expenses/${id}`, {
            method: 'DELETE'
        });
        if (response.ok) loadExpenses();
    } catch (error) {
        console.error('Error deleting:', error);
    }
}