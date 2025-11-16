// Check authentication
checkAuth();

// Display user info
const user = getUser();
document.getElementById('userName').textContent = `${user.firstName} ${user.lastName}`;
document.getElementById('userRole').textContent = user.role;

// Show staff link only for admin
if (isAdmin()) {
    document.getElementById('staffLink').style.display = 'flex';
}

// Load dashboard data
async function loadDashboard() {
    try {
        // Load stats
        const stats = await apiCall('/reports/dashboard');
        
        if (stats.success) {
            document.getElementById('totalBooks').textContent = stats.stats.total_books;
            document.getElementById('totalMembers').textContent = stats.stats.total_members;
            document.getElementById('activeLoans').textContent = stats.stats.active_loans;
            document.getElementById('overdueBooks').textContent = stats.stats.overdue_books;
            document.getElementById('unpaidFines').textContent = stats.stats.unpaid_fines.toFixed(2);
            
            // Display category chart
            displayCategoryChart(stats.stats.books_by_category);
        }
        
        // Load recent loans
        await loadRecentLoans();
        
        // Load fines summary
        await loadFinesSummary();
        
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showError('Failed to load dashboard data');
    }
}

function displayCategoryChart(categories) {
    const container = document.getElementById('categoryChart');
    
    if (!categories || categories.length === 0) {
        container.innerHTML = '<p class="text-muted text-center">No data available</p>';
        return;
    }
    
    const total = categories.reduce((sum, cat) => sum + parseInt(cat.count), 0);
    
    let html = '<div class="category-bars">';
    
    categories.forEach(cat => {
        const percentage = (cat.count / total * 100).toFixed(1);
        html += `
            <div class="category-bar-item">
                <div class="category-info">
                    <span>${cat.category}</span>
                    <span class="badge badge-blue">${cat.count}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: ${percentage}%"></div>
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    container.innerHTML = html;
}

async function loadRecentLoans() {
    try {
        const result = await apiCall('/loans?status=issued');
        
        const container = document.getElementById('recentLoans');
        
        if (!result.loans || result.loans.length === 0) {
            container.innerHTML = '<p class="text-muted text-center">No active loans</p>';
            return;
        }
        
        let html = '<div class="recent-list">';
        
        result.loans.slice(0, 5).forEach(loan => {
            const dueDate = new Date(loan.due_date);
            const today = new Date();
            const isOverdue = dueDate < today;
            
            html += `
                <div class="recent-item">
                    <div class="recent-info">
                        <strong>${loan.book_title}</strong>
                        <p class="text-muted">${loan.member_name}</p>
                    </div>
                    <div class="recent-status">
                        <span class="badge ${isOverdue ? 'badge-red' : 'badge-yellow'}">
                            ${isOverdue ? 'Overdue' : 'Active'}
                        </span>
                        <small class="text-muted">Due: ${loan.due_date}</small>
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
        container.innerHTML = html;
        
    } catch (error) {
        console.error('Error loading recent loans:', error);
    }
}

async function loadFinesSummary() {
    try {
        const result = await apiCall('/fines/total');
        
        if (result.success) {
            document.getElementById('unpaidFines').textContent = result.total_unpaid.toFixed(2);
            document.getElementById('unpaidCount').textContent = result.count;
        }
    } catch (error) {
        console.error('Error loading fines:', error);
    }
}

function showError(message) {
    // Simple error display
    console.error(message);
}

// Load dashboard on page load
loadDashboard();