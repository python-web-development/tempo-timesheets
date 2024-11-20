let worklogs = [];  // To store fetched worklogs globally
const rate_info = {
    'Employee': 50,
    'Contractor': 75
};

function fetchWorklogs(classification) {
    fetch('https://tempo-timesheets.onrender.com/fetch_worklogs/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            from_date: "2021-01-01",
            to_date: "2025-01-31",
            classification: classification  // Send classification to backend if needed
        })
    })
    .then(response => response.json())
    .then(data => {
        worklogs = data.worklogs;  // Store globally
        worklogs.forEach(log => {
            log.total_billing_in_$ = (log.hours_worked * rate_info[classification]).toFixed(2);
        });
        displayWorklogs(worklogs);
        updateTotalAccrual();
    })
    .catch(error => console.error('Error fetching data:', error));
}

function displayWorklogs(worklogs) {
    const container = document.getElementById('worklogsTableContainer');
    let tableHTML = "<table>";
    tableHTML += "<tr><th>ID</th><th>Description</th><th>Date</th><th>Start Time</th><th>Hours Worked</th><th>Total Billing ($)</th><th>AccountId</th></tr>";
    worklogs.forEach(log => {
        tableHTML += `
            <tr>
                <td>${log.tempoWorklogId}</td>
                <td>${log.description}</td>
                <td>${log.startDate}</td>
                <td>${log.startTime}</td>
                <td>${log.hours_worked.toFixed(2)}</td>
                <td>$${log.total_billing_in_$}</td>
                <td>${log.author.accountId}</td>
            </tr>
        `;
    });
    tableHTML += "</table>";
    container.innerHTML = tableHTML;
}

function updateTotalAccrual() {
    const totalAccrual = worklogs.reduce((acc, log) => acc + parseFloat(log.total_billing_in_$), 0);
    document.getElementById('totalAccrual').textContent = `$${totalAccrual.toFixed(2)}`;
}