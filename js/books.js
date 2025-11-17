checkAuth();

const user = getUser();
if (isAdmin()) {
    document.getElementById('staffLink').style.display = 'flex';
    document.getElementById('loginLogsLink').style.display = 'flex';
}
let currentBookId = null;

// Load books on page load
loadBooks();
loadCategories();

async function loadBooks() {
    try {
        const search = document.getElementById('searchInput').value;
        const category = document.getElementById('categoryFilter').value;
        
        let endpoint = '/books?';
        if (search) endpoint += `search=${encodeURIComponent(search)}&`;
        if (category) endpoint += `category=${encodeURIComponent(category)}&`;
        
        const result = await apiCall(endpoint);
        
        const tbody = document.getElementById('booksTable');
        
        if (!result.books || result.books.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" class="text-center text-muted">No books found</td></tr>';
            return;
        }
        
        let html = '';
        result.books.forEach(book => {
            const available = book.quantity > 0;
            html += `
                <tr>
                    <td>${book.isbn}</td>
                    <td><strong>${book.title}</strong></td>
                    <td>${book.author}</td>
                    <td><span class="badge badge-blue">${book.category}</span></td>
                    <td>${book.location || 'N/A'}</td>
                    <td>
                        <span class="badge ${available ? 'badge-green' : 'badge-red'}">
                            ${book.quantity || 0}
                        </span>
                    </td>
                    <td>₹${parseFloat(book.price).toFixed(2)}</td>
                    <td>
                        <button class="btn btn-sm btn-secondary" onclick="editBook(${book.book_id})">Edit</button>
                        <button class="btn btn-sm btn-danger" onclick="deleteBook(${book.book_id}, '${book.title}')">Delete</button>
                    </td>
                </tr>
            `;
        });
        
        tbody.innerHTML = html;
        
    } catch (error) {
        console.error('Error loading books:', error);
        document.getElementById('booksTable').innerHTML = 
            '<tr><td colspan="8" class="text-center text-red">Error loading books</td></tr>';
    }
}

async function loadCategories() {
    try {
        const result = await apiCall('/books/categories');
        
        const select = document.getElementById('categoryFilter');
        
        if (result.success && result.categories) {
            result.categories.forEach(cat => {
                const option = document.createElement('option');
                option.value = cat;
                option.textContent = cat;
                select.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

function showAddModal() {
    currentBookId = null;
    document.getElementById('modalTitle').textContent = 'Add New Book';
    document.getElementById('bookForm').reset();
    document.getElementById('bookId').value = '';
    document.getElementById('bookModal').classList.add('active');
}

async function editBook(bookId) {
    try {
        const result = await apiCall(`/books/${bookId}`);
        
        if (result.success && result.book) {
            currentBookId = bookId;
            document.getElementById('modalTitle').textContent = 'Edit Book';
            document.getElementById('bookId').value = bookId;
            document.getElementById('isbn').value = result.book.isbn;
            document.getElementById('title').value = result.book.title;
            document.getElementById('author').value = result.book.author;
            document.getElementById('category').value = result.book.category;
            document.getElementById('location').value = result.book.location || '';
            document.getElementById('quantity').value = result.book.quantity || 0;
            document.getElementById('price').value = result.book.price;
            
            document.getElementById('bookModal').classList.add('active');
        }
    } catch (error) {
        alert('Error loading book details: ' + error.message);
    }
}

async function saveBook() {
    try {
        const bookData = {
            isbn: document.getElementById('isbn').value,
            title: document.getElementById('title').value,
            author: document.getElementById('author').value,
            category: document.getElementById('category').value,
            location: document.getElementById('location').value,
            quantity: parseInt(document.getElementById('quantity').value),
            price: parseFloat(document.getElementById('price').value)
        };
        
        let result;
        if (currentBookId) {
            result = await apiCall(`/books/${currentBookId}`, 'PUT', bookData);
        } else {
            result = await apiCall('/books', 'POST', bookData);
        }
        
        if (result.success) {
            showModalSuccess(result.message);
            setTimeout(() => {
                closeModal();
                loadBooks();
            }, 1500);
        }
        
    } catch (error) {
        showModalError(error.message);
    }
}

async function deleteBook(bookId, title) {
    if (!confirm(`Are you sure you want to delete "${title}"?`)) {
        return;
    }
    
    try {
        const result = await apiCall(`/books/${bookId}`, 'DELETE');
        
        if (result.success) {
            alert(result.message);
            loadBooks();
        }
    } catch (error) {
        alert('Error deleting book: ' + error.message);
    }
}

function closeModal() {
    document.getElementById('bookModal').classList.remove('active');
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

// Search on Enter key
document.getElementById('searchInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        loadBooks();
    }
});