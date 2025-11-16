from flask import Blueprint, request, jsonify
from database import execute_query, get_db_connection

books_bp = Blueprint('books', __name__)

@books_bp.route('/', methods=['GET'])
def get_books():
    """Get all books with details"""
    try:
        search = request.args.get('search', '')
        category = request.args.get('category', '')
        
        query = """
            SELECT 
                bd.book_detail_id,
                bd.isbn,
                bd.title,
                bd.author,
                bd.category,
                bd.price,
                b.id as book_id,
                b.location,
                b.quantity
            FROM BookDetails bd
            LEFT JOIN Books b ON bd.book_detail_id = b.book_detail_id
            WHERE 1=1
        """
        params = []
        
        if search:
            query += " AND (bd.title LIKE %s OR bd.author LIKE %s OR bd.isbn LIKE %s)"
            search_param = f"%{search}%"
            params.extend([search_param, search_param, search_param])
        
        if category:
            query += " AND bd.category = %s"
            params.append(category)
        
        query += " ORDER BY bd.title"
        
        books = execute_query(query, tuple(params), fetch_all=True)
        return jsonify({'success': True, 'books': books}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@books_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Get single book details"""
    try:
        query = """
            SELECT 
                bd.book_detail_id,
                bd.isbn,
                bd.title,
                bd.author,
                bd.category,
                bd.price,
                b.id as book_id,
                b.location,
                b.quantity
            FROM BookDetails bd
            LEFT JOIN Books b ON bd.book_detail_id = b.book_detail_id
            WHERE b.id = %s
        """
        book = execute_query(query, (book_id,), fetch_one=True)
        
        if book:
            return jsonify({'success': True, 'book': book}), 200
        return jsonify({'error': 'Book not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@books_bp.route('/', methods=['POST'])
def add_book():
    """Add new book"""
    try:
        data = request.get_json()
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Insert into BookDetails
        query1 = """
            INSERT INTO BookDetails (isbn, title, author, category, price)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query1, (
            data['isbn'],
            data['title'],
            data['author'],
            data['category'],
            data['price']
        ))
        book_detail_id = cursor.lastrowid
        
        # Insert into Books
        query2 = """
            INSERT INTO Books (book_detail_id, location, quantity)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query2, (
            book_detail_id,
            data['location'],
            data['quantity']
        ))
        
        connection.commit()
        connection.close()
        
        return jsonify({
            'success': True,
            'message': 'Book added successfully',
            'book_detail_id': book_detail_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@books_bp.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """Update book details"""
    try:
        data = request.get_json()
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Get book_detail_id
        cursor.execute("SELECT book_detail_id FROM Books WHERE id = %s", (book_id,))
        result = cursor.fetchone()
        if not result:
            return jsonify({'error': 'Book not found'}), 404
        
        book_detail_id = result['book_detail_id']
        
        # Update BookDetails
        query1 = """
            UPDATE BookDetails 
            SET isbn = %s, title = %s, author = %s, category = %s, price = %s
            WHERE book_detail_id = %s
        """
        cursor.execute(query1, (
            data['isbn'],
            data['title'],
            data['author'],
            data['category'],
            data['price'],
            book_detail_id
        ))
        
        # Update Books
        query2 = """
            UPDATE Books 
            SET location = %s, quantity = %s
            WHERE id = %s
        """
        cursor.execute(query2, (
            data['location'],
            data['quantity'],
            book_id
        ))
        
        connection.commit()
        connection.close()
        
        return jsonify({'success': True, 'message': 'Book updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@books_bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Delete book"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Check if book is currently loaned
        cursor.execute("""
            SELECT COUNT(*) as count FROM Loans 
            WHERE book_id = %s AND status = 'issued'
        """, (book_id,))
        result = cursor.fetchone()
        
        if result['count'] > 0:
            return jsonify({'error': 'Cannot delete book that is currently loaned'}), 400
        
        # Get book_detail_id
        cursor.execute("SELECT book_detail_id FROM Books WHERE id = %s", (book_id,))
        result = cursor.fetchone()
        if not result:
            return jsonify({'error': 'Book not found'}), 404
        
        book_detail_id = result['book_detail_id']
        
        # Delete from Books
        cursor.execute("DELETE FROM Books WHERE id = %s", (book_id,))
        
        # Delete from BookDetails if no other copies exist
        cursor.execute("SELECT COUNT(*) as count FROM Books WHERE book_detail_id = %s", (book_detail_id,))
        if cursor.fetchone()['count'] == 0:
            cursor.execute("DELETE FROM BookDetails WHERE book_detail_id = %s", (book_detail_id,))
        
        connection.commit()
        connection.close()
        
        return jsonify({'success': True, 'message': 'Book deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@books_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all unique categories"""
    try:
        query = "SELECT DISTINCT category FROM BookDetails ORDER BY category"
        categories = execute_query(query, fetch_all=True)
        return jsonify({
            'success': True,
            'categories': [cat['category'] for cat in categories]
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500