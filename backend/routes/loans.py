 
from flask import Blueprint, request, jsonify
from database import execute_query, get_db_connection
from datetime import datetime, timedelta

loans_bp = Blueprint('loans', __name__)

@loans_bp.route('/', methods=['GET'])
def get_loans():
    """Get all loans with filters"""
    try:
        status = request.args.get('status', '')
        member_id = request.args.get('member_id', '')
        
        query = """
            SELECT 
                l.id,
                l.issue_date,
                l.due_date,
                l.return_date,
                l.status,
                bd.title as book_title,
                bd.author as book_author,
                bd.isbn,
                m.name as member_name,
                m.membership_no,
                CONCAT(u.FirstName, ' ', u.LastName) as issued_by,
                b.id as book_id,
                m.id as member_id
            FROM Loans l
            JOIN Books b ON l.book_id = b.id
            JOIN BookDetails bd ON b.book_detail_id = bd.book_detail_id
            JOIN Members m ON l.member_id = m.id
            JOIN Users u ON l.issued_by = u.id
            WHERE 1=1
        """
        params = []
        
        if status:
            query += " AND l.status = %s"
            params.append(status)
        
        if member_id:
            query += " AND l.member_id = %s"
            params.append(member_id)
        
        query += " ORDER BY l.issue_date DESC"
        
        loans = execute_query(query, tuple(params), fetch_all=True)
        
        # Convert dates to strings
        for loan in loans:
            if loan['issue_date']:
                loan['issue_date'] = loan['issue_date'].strftime('%Y-%m-%d')
            if loan['due_date']:
                loan['due_date'] = loan['due_date'].strftime('%Y-%m-%d')
            if loan['return_date']:
                loan['return_date'] = loan['return_date'].strftime('%Y-%m-%d')
        
        return jsonify({'success': True, 'loans': loans}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@loans_bp.route('/<int:loan_id>', methods=['GET'])
def get_loan(loan_id):
    """Get single loan details"""
    try:
        query = """
            SELECT 
                l.*,
                bd.title as book_title,
                bd.author as book_author,
                m.name as member_name,
                CONCAT(u.FirstName, ' ', u.LastName) as issued_by_name
            FROM Loans l
            JOIN Books b ON l.book_id = b.id
            JOIN BookDetails bd ON b.book_detail_id = bd.book_detail_id
            JOIN Members m ON l.member_id = m.id
            JOIN Users u ON l.issued_by = u.id
            WHERE l.id = %s
        """
        loan = execute_query(query, (loan_id,), fetch_one=True)
        
        if loan:
            if loan['issue_date']:
                loan['issue_date'] = loan['issue_date'].strftime('%Y-%m-%d')
            if loan['due_date']:
                loan['due_date'] = loan['due_date'].strftime('%Y-%m-%d')
            if loan['return_date']:
                loan['return_date'] = loan['return_date'].strftime('%Y-%m-%d')
            return jsonify({'success': True, 'loan': loan}), 200
        return jsonify({'error': 'Loan not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@loans_bp.route('/issue', methods=['POST'])
def issue_book():
    """Issue a book to a member"""
    try:
        data = request.get_json()
        book_id = data.get('book_id')
        member_id = data.get('member_id')
        issued_by = data.get('issued_by')
        
        if not all([book_id, member_id, issued_by]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Check if book is available
        cursor.execute("SELECT quantity FROM Books WHERE id = %s", (book_id,))
        book = cursor.fetchone()
        
        if not book or book['quantity'] <= 0:
            connection.close()
            return jsonify({'error': 'Book not available'}), 400
        
        # Check if member has overdue books
        cursor.execute("""
            SELECT COUNT(*) as count FROM Loans 
            WHERE member_id = %s AND status = 'overdue'
        """, (member_id,))
        
        if cursor.fetchone()['count'] > 0:
            connection.close()
            return jsonify({'error': 'Member has overdue books'}), 400
        
        # Calculate dates
        issue_date = datetime.now().date()
        due_date = issue_date + timedelta(days=14)  # 14 days loan period
        
        # Create loan record
        cursor.execute("""
            INSERT INTO Loans (book_id, member_id, issued_by, issue_date, due_date, status)
            VALUES (%s, %s, %s, %s, %s, 'issued')
        """, (book_id, member_id, issued_by, issue_date, due_date))
        
        loan_id = cursor.lastrowid
        
        # Decrease book quantity
        cursor.execute("""
            UPDATE Books SET quantity = quantity - 1 WHERE id = %s
        """, (book_id,))
        
        connection.commit()
        connection.close()
        
        return jsonify({
            'success': True,
            'message': 'Book issued successfully',
            'loan_id': loan_id,
            'due_date': due_date.strftime('%Y-%m-%d')
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@loans_bp.route('/<int:loan_id>/return', methods=['PUT'])
def return_book(loan_id):
    """Return a book"""
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Get loan details
        cursor.execute("""
            SELECT book_id, due_date, status FROM Loans WHERE id = %s
        """, (loan_id,))
        loan = cursor.fetchone()
        
        if not loan:
            connection.close()
            return jsonify({'error': 'Loan not found'}), 404
        
        if loan['status'] == 'returned':
            connection.close()
            return jsonify({'error': 'Book already returned'}), 400
        
        return_date = datetime.now().date()
        
        # Update loan status
        cursor.execute("""
            UPDATE Loans 
            SET return_date = %s, status = 'returned'
            WHERE id = %s
        """, (return_date, loan_id))
        
        # Increase book quantity
        cursor.execute("""
            UPDATE Books SET quantity = quantity + 1 WHERE id = %s
        """, (loan['book_id'],))
        
        # Calculate fine if overdue
        fine_amount = 0
        if return_date > loan['due_date']:
            days_late = (return_date - loan['due_date']).days
            fine_amount = days_late * 5  # ₹5 per day
            
            # Create or update fine record
            cursor.execute("""
                INSERT INTO Fines (loan_id, fine_amount, paid)
                VALUES (%s, %s, 'unpaid')
                ON DUPLICATE KEY UPDATE fine_amount = %s
            """, (loan_id, fine_amount, fine_amount))
        
        connection.commit()
        connection.close()
        
        return jsonify({
            'success': True,
            'message': 'Book returned successfully',
            'fine_amount': fine_amount
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@loans_bp.route('/overdue', methods=['GET'])
def get_overdue_loans():
    """Get all overdue loans"""
    try:
        query = """
            SELECT 
                l.id,
                l.issue_date,
                l.due_date,
                bd.title as book_title,
                m.name as member_name,
                m.phone,
                DATEDIFF(CURDATE(), l.due_date) as days_overdue
            FROM Loans l
            JOIN Books b ON l.book_id = b.id
            JOIN BookDetails bd ON b.book_detail_id = bd.book_detail_id
            JOIN Members m ON l.member_id = m.id
            WHERE l.due_date < CURDATE() AND l.status = 'issued'
            ORDER BY l.due_date ASC
        """
        loans = execute_query(query, fetch_all=True)
        
        # Convert dates
        for loan in loans:
            if loan['issue_date']:
                loan['issue_date'] = loan['issue_date'].strftime('%Y-%m-%d')
            if loan['due_date']:
                loan['due_date'] = loan['due_date'].strftime('%Y-%m-%d')
        
        return jsonify({'success': True, 'overdue_loans': loans}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500