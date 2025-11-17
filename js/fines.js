checkAuth();

const user = getUser();
if (isAdmin()) {
    document.getElementById('staffLink').style.display = 'flex';
    document.getElementById('loginLogsLink').style.display = 'flex';
}

loadFines();
loadTotalFines();

async function loadFines() {
    try {
        const status = document.getElementById('statusFilter').value;
        let endpoint = '/fines?';
        if (status) endpoint += `status=${status}`;
        
        const result = await apiCall(endpoint);
        
        const tbody = document.getElementById('finesTable');
        
        if (!result.fines || result.fines.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted">No fines found</td></tr>';
            return;
        }
        
        let html = '';
        result.fines.forEach(fine => {
            const isPaid = fine.paid === 'paid';
            
            html += `
                <tr>
                    <td><strong>#${fine.id}</strong></td>
                    <td>${fine.member_name}<br><small class="text-muted">${fine.membership_no}</small></td>
                    <td>${fine.book_title}</td>
                    <td>${fine.due_date}</td>
                    <td>${fine.return_date || '-'}</td>
                    <td><strong class="text-red">₹${parseFloat(fine.fine_amount).toFixed(2)}</strong></td>
                    <td>
                        <span class="badge ${isPaid ? 'badge-green' : 'badge-red'}">
                            ${isPaid ? 'Paid' : 'Unpaid'}
                        </span>
                    </td>
                    <td>
                        ${!isPaid ? 
                            `<button class="btn btn-sm btn-success" onclick="markAsPaid(${fine.id})">Mark as Paid</button>` :
                            '-'
                        }
                    </td>
                </tr>
            `;
        });
        
        tbody.innerHTML = html;
        
    } catch (error) {
        console.error('Error loading fines:', error);
        document.getElementById('finesTable').innerHTML = 
            '<tr><td colspan="8" class="text-center text-red">Error loading fines</td></tr>';
    }
}

async function loadTotalFines() {
    try {
        const result = await apiCall('/fines/total');
        
        if (result.success) {
            document.getElementById('totalUnpaid').textContent = result.total_unpaid.toFixed(2);
            document.getElementById('unpaidCount').textContent = result.count;
        }
    } catch (error) {
        console.error('Error loading total fines:', error);
    }
}

async function markAsPaid(fineId) {
    if (!confirm('Are you sure you want to mark this fine as paid?')) {
        return;
    }
    
    try {
        const result = await apiCall(`/fines/${fineId}/pay`, 'PUT');
        
        if (result.success) {
            alert('Fine marked as paid successfully!');
            loadFines();
            loadTotalFines();
        }
    } catch (error) {
        alert('Error marking fine as paid: ' + error.message);
    }
}