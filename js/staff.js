checkAuth();

const user = getUser();

if (isAdmin()) {
    document.getElementById('staffLink').style.display = 'flex';
    document.getElementById('loginLogsLink').style.display = 'flex';
}

// Check if user is Admin
if (!isAdmin()) {
    alert('Access denied. Admin only.');
    window.location.href = 'dashboard.html';
}

let currentStaffId = null;

loadStaff();

async function loadStaff() {
    try {
        const result = await apiCall('/staff');
        
        const tbody = document.getElementById('staffTable');
        
        if (!result.staff || result.staff.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">No staff found</td></tr>';
            return;
        }
        
        let html = '';
        result.staff.forEach(staff => {
            let roleBadge = '';
            if (staff.Role === 'Admin') {
                roleBadge = '<span class="badge badge-red">Admin</span>';
            } else if (staff.Role === 'Librarian') {
                roleBadge = '<span class="badge badge-blue">Librarian</span>';
            } else {
                roleBadge = '<span class="badge badge-yellow">Assistant</span>';
            }
            
            html += `
                <tr>
                    <td><strong>#${staff.StaffID}</strong></td>
                    <td>${staff.FirstName} ${staff.LastName}</td>
                    <td>${staff.Username}</td>
                    <td>${roleBadge}</td>
                    <td>
                        <button class="btn btn-sm btn-secondary" onclick="editStaff(${staff.StaffID})">Edit</button>
                        ${staff.StaffID !== user.id ? 
                            `<button class="btn btn-sm btn-danger" onclick="deleteStaff(${staff.StaffID}, '${staff.FirstName} ${staff.LastName}')">Delete</button>` :
                            '<span class="text-muted">Current User</span>'
                        }
                    </td>
                </tr>
            `;
        });
        
        tbody.innerHTML = html;
        
    } catch (error) {
        console.error('Error loading staff:', error);
        document.getElementById('staffTable').innerHTML = 
            '<tr><td colspan="5" class="text-center text-red">Error loading staff</td></tr>';
    }
}

function showAddModal() {
    currentStaffId = null;
    document.getElementById('modalTitle').textContent = 'Add New Staff';
    document.getElementById('staffForm').reset();
    document.getElementById('staffId').value = '';
    document.getElementById('password').required = true;
    document.getElementById('staffModal').classList.add('active');
}

async function editStaff(staffId) {
    try {
        const result = await apiCall(`/staff/${staffId}`);
        
        if (result.success && result.staff) {
            currentStaffId = staffId;
            document.getElementById('modalTitle').textContent = 'Edit Staff';
            document.getElementById('staffId').value = staffId;
            document.getElementById('firstName').value = result.staff.FirstName;
            document.getElementById('lastName').value = result.staff.LastName;
            document.getElementById('username').value = result.staff.Username;
            document.getElementById('role').value = result.staff.Role;
            document.getElementById('password').required = false;
            document.getElementById('password').placeholder = 'Leave blank to keep current password';
            
            document.getElementById('staffModal').classList.add('active');
        }
    } catch (error) {
        alert('Error loading staff details: ' + error.message);
    }
}

async function saveStaff() {
    try {
        const staffData = {
            firstName: document.getElementById('firstName').value,
            lastName: document.getElementById('lastName').value,
            username: document.getElementById('username').value,
            role: document.getElementById('role').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value
        };
        
        const password = document.getElementById('password').value;
        if (password) {
            staffData.password = password;
        }
        
        let result;
        if (currentStaffId) {
            result = await apiCall(`/staff/${currentStaffId}`, 'PUT', staffData);
        } else {
            if (!password) {
                showModalError('Password is required for new staff');
                return;
            }
            staffData.password = password;
            result = await apiCall('/staff', 'POST', staffData);
        }
        
        if (result.success) {
            showModalSuccess(result.message);
            setTimeout(() => {
                closeModal();
                loadStaff();
            }, 1500);
        }
        
    } catch (error) {
        showModalError(error.message);
    }
}

async function deleteStaff(staffId, name) {
    if (!confirm(`Are you sure you want to delete staff member "${name}"?`)) {
        return;
    }
    
    try {
        const result = await apiCall(`/staff/${staffId}`, 'DELETE');
        
        if (result.success) {
            alert(result.message);
            loadStaff();
        }
    } catch (error) {
        alert('Error deleting staff: ' + error.message);
    }
}

function closeModal() {
    document.getElementById('staffModal').classList.remove('active');
    document.getElementById('modalError').style.display = 'none';
    document.getElementById('modalSuccess').style.display = 'none';
    document.getElementById('password').required = true;
    document.getElementById('password').placeholder = '';
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