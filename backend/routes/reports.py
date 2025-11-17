from flask import Blueprint, request, jsonify
from database import execute_query

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/dashboard', methods=['GET'])
def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        stats = {}
        
        # Total books
        result = execute_query("SELECT COALESCE(SUM(quantity), 0) as total FROM Books", fetch_one=True)
        stats['total_books'] = int(result['total']) if result and result['total'] else 0
        
        # Total members
        result = execute_query("SELECT COUNT(*) as total FROM Members WHERE active = 1", fetch_one=True)
        stats['total_members'] = int(result['total']) if result else 0
        
        # Active loans
        result = execute_query("SELECT COUNT(*) as total FROM Loans WHERE status = 'issued'", fetch_one=True)
        stats['active_loans'] = int(result['total']) if result else 0
        
        # Overdue books
        result = execute_query("""
            SELECT COUNT(*) as total FROM Loans 
            WHERE due_date < CURDATE() AND status = 'issued'
        """, fetch_one=True)
        stats['overdue_books'] = int(result['total']) if result else 0
        
        # Total fines unpaid
        result = execute_query("""
            SELECT COALESCE(SUM(fine_amount), 0) as total FROM Fines WHERE paid = 'unpaid'
        """, fetch_one=True)
        stats['unpaid_fines'] = float(result['total']) if result and result['total'] else 0.0
        
        # Books by category
        categories = execute_query("""
            SELECT bd.category, COALESCE(SUM(b.quantity), 0) as count
            FROM BookDetails bd
            LEFT JOIN Books b ON bd.book_detail_id = b.book_detail_id
            GROUP BY bd.category
            ORDER BY count DESC
        """, fetch_all=True)
        
        stats['books_by_category'] = []
        if categories:
            for cat in categories:
                stats['books_by_category'].append({
                    'category': cat['category'],
                    'count': int(cat['count']) if cat['count'] else 0
                })
        
        return jsonify({'success': True, 'stats': stats}), 200
        
    except Exception as e:
        print(f"Dashboard stats error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@reports_bp.route('/most-borrowed', methods=['GET'])
def get_most_borrowed():
    """Get most borrowed books"""
    try:
        limit = int(request.args.get('limit', 10))
        
        query = """
            SELECT 
                bd.title,
                bd.author,
                bd.category,
                COUNT(l.id) as borrow_count
            FROM Loans l
            JOIN Books b ON l.book_id = b.id
            JOIN BookDetails bd ON b.book_detail_id = bd.book_detail_id
            GROUP BY bd.book_detail_id, bd.title, bd.author, bd.category
            HAVING borrow_count > 0
            ORDER BY borrow_count DESC
            LIMIT %s
        """
        books = execute_query(query, (limit,), fetch_all=True)
        
        result = []
        if books:
            for book in books:
                result.append({
                    'title': book['title'],
                    'author': book['author'],
                    'category': book['category'],
                    'borrow_count': int(book['borrow_count'])
                })
        
        return jsonify({'success': True, 'books': result}), 200
        
    except Exception as e:
        print(f"Most borrowed error: {str(e)}")
        return jsonify({'success': True, 'error': str(e), 'books': []}), 200

@reports_bp.route('/active-members', methods=['GET'])
def get_active_members():
    """Get most active members"""
    try:
        limit = int(request.args.get('limit', 10))
        
        query = """
            SELECT 
                m.name,
                m.membership_no,
                m.email,
                COUNT(l.id) as borrow_count
            FROM Loans l
            JOIN Members m ON l.member_id = m.id
            GROUP BY m.id, m.name, m.membership_no, m.email
            HAVING borrow_count > 0
            ORDER BY borrow_count DESC
            LIMIT %s
        """
        members = execute_query(query, (limit,), fetch_all=True)
        
        result = []
        if members:
            for member in members:
                result.append({
                    'name': member['name'],
                    'membership_no': member['membership_no'],
                    'email': member['email'],
                    'borrow_count': int(member['borrow_count'])
                })
        
        return jsonify({'success': True, 'members': result}), 200
        
    except Exception as e:
        print(f"Active members error: {str(e)}")
        return jsonify({'success': True, 'error': str(e), 'members': []}), 200

@reports_bp.route('/monthly-stats', methods=['GET'])
def get_monthly_stats():
    """Get monthly borrowing statistics"""
    try:
        query = """
            SELECT 
                DATE_FORMAT(issue_date, '%%Y-%%m') as month,
                COUNT(*) as total_issues,
                SUM(CASE WHEN status = 'returned' THEN 1 ELSE 0 END) as total_returns
            FROM Loans
            WHERE issue_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
            GROUP BY DATE_FORMAT(issue_date, '%%Y-%%m')
            ORDER BY month DESC
        """
        stats = execute_query(query, fetch_all=True)
        
        result = []
        if stats:
            for stat in stats:
                result.append({
                    'month': stat['month'],
                    'total_issues': int(stat['total_issues']) if stat['total_issues'] else 0,
                    'total_returns': int(stat['total_returns']) if stat['total_returns'] else 0
                })
        
        return jsonify({'success': True, 'monthly_stats': result}), 200
        
    except Exception as e:
        print(f"Monthly stats error: {str(e)}")
        return jsonify({'success': True, 'error': str(e), 'monthly_stats': []}), 200

@reports_bp.route('/late-returns', methods=['GET'])
def get_late_return_trends():
    """Get late return trends"""
    try:
        query = """
            SELECT 
                m.name,
                m.membership_no,
                COUNT(*) as late_count,
                AVG(DATEDIFF(l.return_date, l.due_date)) as avg_late_days
            FROM Loans l
            JOIN Members m ON l.member_id = m.id
            WHERE l.return_date IS NOT NULL AND l.return_date > l.due_date
            GROUP BY m.id, m.name, m.membership_no
            HAVING late_count > 0
            ORDER BY avg_late_days DESC
        """
        trends = execute_query(query, fetch_all=True)
        
        result = []
        if trends:
            for trend in trends:
                result.append({
                    'name': trend['name'],
                    'membership_no': trend['membership_no'],
                    'late_count': int(trend['late_count']) if trend['late_count'] else 0,
                    'avg_late_days': float(trend['avg_late_days']) if trend['avg_late_days'] else 0.0
                })
        
        return jsonify({'success': True, 'late_return_trends': result}), 200
        
    except Exception as e:
        print(f"Late returns error: {str(e)}")
        return jsonify({'success': True, 'error': str(e), 'late_return_trends': []}), 200