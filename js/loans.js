checkAuth();

const user = getUser();
if (isAdmin()) {
    document.getElementById('staffLink').style.display = 'flex';
}

loadLoans();

async function loadLoans() {
    try {
        const status = document.getElementById('statusFilter').value;
        let endpoint = '/loans?';
        if (status) endpoint += `status=${status}`;
        
        const result = await apiCall(endpoint);
        
        const tbody = document.getElementById('loansTable');
        
        if (!result.loans || result.loans.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted">No loans found</td></tr>';
            return;
        }
        
        let html = '';
        result.loans.forEach(loan => {
            const dueDate = new Date(loan.due_date);
            const today = new Date();
            const isOverdue = loan.status === 'issued' && dueDate < today;
            
            let statusBadge = '';
            if (loan.status === 'returned') {
                statusBadge = '<span class="badge badge-green">Returned</span>';
            } else if (isOverdue) {
                statusBadge = '<span class="badge badge-red">Overdue</span>';
            } else {
                statusBadge = '<span class="badge badge-yellow">Issued</span>';
            }
            
            html += `
                <tr>
                    <td><strong>#${loan.id}</strong></td>
                    <td>${loan.book_title}</td>
                    <td>${loan.member_name}</td>
                    <td>${loan.issue_date}</td>
                    <td>${loan.due_date}</td>
                    <td>${loan.return_date || '-'}</td>
                    <td>${statusBadge}</td>
                    <td>
                        ${loan.status === 'issued' ? 
                            `<button class="btn btn-sm btn-success" onclick="returnBook(${loan.id})">Return</button>` :
                            '-'
                        }
                    </td>
                </tr>
            `;
        });
        
        tbody.innerHTML = html;
        
    } catch (error) {
        console.error('Error loading loans:', error);
        document.getElementById('loansTable').innerHTML = 
            '<tr><td colspan="8" class="text-center text-red">Error loading loans</td></tr>';
    }
}

async function showIssueModal() {
    document.getElementById('issueModal').classList.add('active');
    
    // Load books
    try {
        const booksResult = await apiCall('/books');
        const bookSelect = document.getElementById('bookSelect');
        bookSelect.innerHTML = '<option value="">Select a book</option>';
        
        if (booksResult.books) {
            booksResult.books
                .filter(book => book.quantity > 0)
                .forEach(book => {
                    const option = document.createElement('option');
                    option.value = book.book_id;
                    option.textContent = `${book.title} - ${book.author} (Available: ${book.quantity})`;
                    bookSelect.appendChild(option);
                });
        }
    } catch (error) {
        console.error('Error loading books:', error);
    }
    
    // Load members
    try {
        const membersResult = await apiCall('/members?active=true');
        const memberSelect = document.getElementById('memberSelect');
        memberSelect.innerHTML = '<option value="">Select a member</option>';
        
        if (membersResult.members) {
            membersResult.members.forEach(member => {
                const option = document.createElement('option');
                option.value = member.id;
                option.textContent = `${member.name} (${member.membership_no})`;
                memberSelect.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading members:', error);
    }
}

async function issueBook() {
    try {
        const bookId = document.getElementById('bookSelect').value;
        const memberId = document.getElementById('memberSelect').value;
        
        if (!bookId || !memberId) {
            showModalError('Please select both book and member');
            return;
        }
        
        const result = await apiCall('/loans/issue', 'POST', {
            book_id: parseInt(bookId),
            member_id: parseInt(memberId),
            issued_by: user.id
        });
        
        if (result.success) {
            showModalSuccess(`Book issued successfully. Due date: ${result.due_date}`);
            setTimeout(() => {
                closeModal();
                loadLoans();
            }, 2000);
        }
        
    } catch (error) {
        showModalError(error.message);
    }
}

async function returnBook(loanId) {
    if (!confirm('Are you sure you want to mark this book as returned?')) {
        return;
    }
    
    try {
        const result = await apiCall(`/loans/${loanId}/return`, 'PUT');
        
        if (result.success) {
            let message = 'Book returned successfully!';
            if (result.fine_amount > 0) {
                message += ` Fine: ₹${result.fine_amount.toFixed(2)}`;
            }
            alert(message);
            loadLoans();
        }
    } catch (error) {
        alert('Error returning book: ' + error.message);
    }
}

function closeModal() {
    document.getElementById('issueModal').classList.remove('active');
    document.getElementById('modalError').style.display = 'none';
    document.getElementById('modalSuccess').style.display = 'none';
}

function showModalError(message) {
    const errorDiv = document.getElementById('modalError');
    errorDiv.textContent = message;
    errorDiv.style.display = 'block';
    document.getElementById('modalSuccess').style.display = 'none';
}

function showModalSuccess(message) {
    const successDiv = document.getElementById('modalSuccess');
    successDiv.textContent = message;
    successDiv.style.display = 'block';
    document.getElementById('modalError').style.display = 'none';
}