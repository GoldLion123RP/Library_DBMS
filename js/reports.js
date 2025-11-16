checkAuth();

const user = getUser();
if (isAdmin()) {
    document.getElementById('staffLink').style.display = 'flex';
}

loadMostBorrowed();
loadActiveMembers();
loadLateReturns();
loadMonthlyStats();

async function loadMostBorrowed() {
    try {
        const result = await apiCall('/reports/most-borrowed?limit=10');
        
        const tbody = document.getElementById('mostBorrowedTable');
        
        if (!result.books || result.books.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">No data available</td></tr>';
            return;
        }
        
        let html = '';
        result.books.forEach((book, index) => {
            html += `
                <tr>
                    <td><strong>#${index + 1}</strong></td>
                    <td>${book.title}</td>
                    <td>${book.author}</td>
                    <td><span class="badge badge-blue">${book.category}</span></td>
                    <td><strong>${book.borrow_count}</strong></td>
                </tr>
            `;
        });
        
        tbody.innerHTML = html;
        
    } catch (error) {
        console.error('Error loading most borrowed:', error);
        document.getElementById('mostBorrowedTable').innerHTML = 
            '<tr><td colspan="5" class="text-center text-red">Error loading data</td></tr>';
    }
}

async function loadActiveMembers() {
    try {
        const result = await apiCall('/reports/active-members?limit=10');
        
        const tbody = document.getElementById('activeMembersTable');
        
        if (!result.members || result.members.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">No data available</td></tr>';
            return;
        }
        
        let html = '';
        result.members.forEach((member, index) => {
            html += `
                <tr>
                    <td><strong>#${index + 1}</strong></td>
                    <td>${member.name}</td>
                    <td>${member.membership_no}</td>
                    <td>${member.email}</td>
                    <td><span class="badge badge-green">${member.borrow_count}</span></td>
                </tr>
            `;
        });
        
        tbody.innerHTML = html;
        
    } catch (error) {
        console.error('Error loading active members:', error);
        document.getElementById('activeMembersTable').innerHTML = 
            '<tr><td colspan="5" class="text-center text-red">Error loading data</td></tr>';
    }
}

async function loadLateReturns() {
    try {
        const result = await apiCall('/reports/late-returns');
        
        const tbody = document.getElementById('lateReturnsTable');
        
        if (!result.late_return_trends || result.late_return_trends.length === 0) {
            tbody.innerHTML = '<tr><td colspan="4" class="text-center text-muted">No late returns recorded</td></tr>';
            return;
        }
        
        let html = '';
        result.late_return_trends.forEach(trend => {
            html += `
                <tr>
                    <td>${trend.name}</td>
                    <td>${trend.membership_no}</td>
                    <td><span class="badge badge-yellow">${trend.late_count}</span></td>
                    <td><span class="badge badge-red">${parseFloat(trend.avg_late_days).toFixed(1)} days</span></td>
                </tr>
            `;
        });
        
        tbody.innerHTML = html;
        
    } catch (error) {
        console.error('Error loading late returns:', error);
        document.getElementById('lateReturnsTable').innerHTML = 
            '<tr><td colspan="4" class="text-center text-red">Error loading data</td></tr>';
    }
}

async function loadMonthlyStats() {
    try {
        const result = await apiCall('/reports/monthly-stats');
        
        const tbody = document.getElementById('monthlyStatsTable');
        
        if (!result.monthly_stats || result.monthly_stats.length === 0) {
            tbody.innerHTML = '<tr><td colspan="3" class="text-center text-muted">No data available</td></tr>';
            return;
        }
        
        let html = '';
        result.monthly_stats.forEach(stat => {
            html += `
                <tr>
                    <td><strong>${stat.month}</strong></td>
                    <td><span class="badge badge-blue">${stat.total_issues}</span></td>
                    <td><span class="badge badge-green">${stat.total_returns}</span></td>
                </tr>
            `;
        });
        
        tbody.innerHTML = html;
        
    } catch (error) {
        console.error('Error loading monthly stats:', error);
        document.getElementById('monthlyStatsTable').innerHTML = 
            '<tr><td colspan="3" class="text-center text-red">Error loading data</td></tr>';
    }
}