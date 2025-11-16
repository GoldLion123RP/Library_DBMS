checkAuth();

const user = getUser();
if (isAdmin()) {
    document.getElementById('staffLink').style.display = 'flex';
}

let currentMemberId = null;

loadMembers();

async function loadMembers() {
    try {
        const search = document.getElementById('searchInput').value;
        let endpoint = '/members?';
        if (search) endpoint += `search=${encodeURIComponent(search)}`;
        
        const result = await apiCall(endpoint);
        
        const tbody = document.getElementById('membersTable');
        
        if (!result.members || result.members.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted">No members found</td></tr>';
            return;
        }
        
        let html = '';
        result.members.forEach(member => {
            const isActive = member.active === 1 || member.active === true;
            html += `
                <tr>
                    <td><strong>${member.membership_no}</strong></td>
                    <td>${member.name}</td>
                    <td>${member.email}</td>
                    <td>${member.phone}</td>
                    <td>${member.join_date}</td>
                    <td>
                        <span class="badge ${isActive ? 'badge-green' : 'badge-red'}">
                            ${isActive ? 'Active' : 'Inactive'}
                        </span>
                    </td>
                    <td>
                        <button class="btn btn-sm btn-secondary" onclick="editMember(${member.id})">Edit</button>
                        <button class="btn btn-sm btn-danger" onclick="deleteMember(${member.id}, '${member.name}')">Delete</button>
                    </td>
                </tr>
            `;
        });
        
        tbody.innerHTML = html;
        
    } catch (error) {
        console.error('Error loading members:', error);
        document.getElementById('membersTable').innerHTML = 
            '<tr><td colspan="7" class="text-center text-red">Error loading members</td></tr>';
    }
}

function showAddModal() {
    currentMemberId = null;
    document.getElementById('modalTitle').textContent = 'Add New Member';
    document.getElementById('memberForm').reset();
    document.getElementById('memberId').value = '';
    document.getElementById('joinDate').value = new Date().toISOString().split('T')[0];
    document.getElementById('active').checked = true;
    document.getElementById('memberModal').classList.add('active');
}

async function editMember(memberId) {
    try {
        const result = await apiCall(`/members/${memberId}`);
        
        if (result.success && result.member) {
            currentMemberId = memberId;
            document.getElementById('modalTitle').textContent = 'Edit Member';
            document.getElementById('memberId').value = memberId;
            document.getElementById('membershipNo').value = result.member.membership_no;
            document.getElementById('name').value = result.member.name;
            document.getElementById('email').value = result.member.email;
            document.getElementById('phone').value = result.member.phone;
            document.getElementById('joinDate').value = result.member.join_date;
            document.getElementById('active').checked = result.member.active === 1;
            
            document.getElementById('memberModal').classList.add('active');
        }
    } catch (error) {
        alert('Error loading member details: ' + error.message);
    }
}

async function saveMember() {
    try {
        const memberData = {
            membership_no: document.getElementById('membershipNo').value,
            name: document.getElementById('name').value,
            email: document.getElementById('email').value,
            phone: document.getElementById('phone').value,
            join_date: document.getElementById('joinDate').value,
            active: document.getElementById('active').checked ? 1 : 0
        };
        
        let result;
        if (currentMemberId) {
            result = await apiCall(`/members/${currentMemberId}`, 'PUT', memberData);
        } else {
            result = await apiCall('/members', 'POST', memberData);
        }
        
        if (result.success) {
            showModalSuccess(result.message);
            setTimeout(() => {
                closeModal();
                loadMembers();
            }, 1500);
        }
        
    } catch (error) {
        showModalError(error.message);
    }
}

async function deleteMember(memberId, name) {
    if (!confirm(`Are you sure you want to delete member "${name}"?`)) {
        return;
    }
    
    try {
        const result = await apiCall(`/members/${memberId}`, 'DELETE');
        
        if (result.success) {
            alert(result.message);
            loadMembers();
        }
    } catch (error) {
        alert('Error deleting member: ' + error.message);
    }
}

function closeModal() {
    document.getElementById('memberModal').classList.remove('active');
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

document.getElementById('searchInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        loadMembers();
    }
});