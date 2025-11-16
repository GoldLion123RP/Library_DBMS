 
from flask import Blueprint, request, jsonify
from database import execute_query

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/dashboard', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        stats = {}
        
        # Total books
        result = execute_query("SELECT SUM(quantity) as total FROM Books", fetch_one=True)
        stats['total_books'] = result['total'] or 0
        
        # Total members
        result = execute_query("SELECT COUNT(*) as total FROM Members WHERE active = 1", fetch_one=True)
        stats['total_members'] = result['total'] or 0
        
        # Active loans
        result = execute_query("SELECT COUNT(*) as total FROM Loans WHERE status = 'issued'", fetch_one=True)
        stats['active_loans'] = result['total'] or 0
        
        # Overdue books
        result = execute_query("""
            SELECT COUNT(*) as total FROM Loans 
            WHERE due_date < CURDATE() AND status = 'issued'
        """, fetch_one=True)
        stats['overdue_books'] = result['total'] or 0
        
        # Total fines unpaid
        result = execute_query("""
            SELECT SUM(fine_amount) as total FROM Fines WHERE paid = 'unpaid'
        """, fetch_one=True)
        stats['unpaid_fines'] = float(result['total'] or 0)
        
        # Books by category
        categories = execute_query("""
            SELECT bd.category, SUM(b.quantity) as count
            FROM BookDetails bd
            JOIN Books b ON bd.book_detail_id = b.book_detail_id
            GROUP BY bd.category
            ORDER BY count DESC
        """, fetch_all=True)
        stats['books_by_category'] = categories
        
        return jsonify({'success': True, 'stats': stats}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/most-borrowed', methods=['GET'])
def get_most_borrowed():
    """Get most borrowed books"""
    try:
        limit = request.args.get('limit', 10)
        
        query = """
            SELECT 
                bd.title,
                bd.author,
                bd.category,
                COUNT(*) as borrow_count
            FROM Loans l
            JOIN Books b ON l.book_id = b.id
            JOIN BookDetails bd ON b.book_detail_id = bd.book_detail_id
            GROUP BY bd.book_detail_id, bd.title, bd.author, bd.category
            ORDER BY borrow_count DESC
            LIMIT %s
        """
        books = execute_query(query, (limit,), fetch_all=True)
        
        return jsonify({'success': True, 'books': books}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/active-members', methods=['GET'])
def get_active_members():
    """Get most active members"""
    try:
        limit = request.args.get('limit', 10)
        
        query = """
            SELECT 
                m.name,
                m.membership_no,
                m.email,
                COUNT(*) as borrow_count
            FROM Loans l
            JOIN Members m ON l.member_id = m.id
            GROUP BY m.id, m.name, m.membership_no, m.email
            ORDER BY borrow_count DESC
            LIMIT %s
        """
        members = execute_query(query, (limit,), fetch_all=True)
        
        return jsonify({'success': True, 'members': members}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/monthly-stats', methods=['GET'])
def get_monthly_stats():
    """Get monthly borrowing statistics"""
    try:
        query = """
            SELECT 
                DATE_FORMAT(issue_date, '%Y-%m') as month,
                COUNT(*) as total_issues,
                SUM(CASE WHEN status = 'returned' THEN 1 ELSE 0 END) as total_returns
            FROM Loans
            WHERE issue_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
            GROUP BY DATE_FORMAT(issue_date, '%Y-%m')
            ORDER BY month DESC
        """
        stats = execute_query(query, fetch_all=True)
        
        return jsonify({'success': True, 'monthly_stats': stats}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/late-returns', methods=['GET'])
def get_late_return_trends():
    """Get late return trends"""
    try:
        query = """
            SELECT 
                m.name,
                m.membership_no,
                AVG(DATEDIFF(l.return_date, l.due_date)) as avg_late_days,
                COUNT(*) as late_count
            FROM Loans l
            JOIN Members m ON l.member_id = m.id
            WHERE l.return_date > l.due_date
            GROUP BY m.id, m.name, m.membership_no
            HAVING late_count > 0
            ORDER BY avg_late_days DESC
        """
        trends = execute_query(query, fetch_all=True)
        
        # Convert avg_late_days to float
        for trend in trends:
            trend['avg_late_days'] = float(trend['avg_late_days'] or 0)
        
        return jsonify({'success': True, 'late_return_trends': trends}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500