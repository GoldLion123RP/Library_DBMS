 
from flask import Blueprint, request, jsonify
from database import execute_query

fines_bp = Blueprint('fines', __name__)

@fines_bp.route('/', methods=['GET'])
def get_fines():
    """Get all fines"""
    try:
        status = request.args.get('status', '')
        
        query = """
            SELECT 
                f.id,
                f.loan_id,
                f.fine_amount,
                f.paid,
                l.issue_date,
                l.due_date,
                l.return_date,
                bd.title as book_title,
                m.name as member_name,
                m.membership_no
            FROM Fines f
            JOIN Loans l ON f.loan_id = l.id
            JOIN Books b ON l.book_id = b.id
            JOIN BookDetails bd ON b.book_detail_id = bd.book_detail_id
            JOIN Members m ON l.member_id = m.id
            WHERE 1=1
        """
        params = []
        
        if status:
            query += " AND f.paid = %s"
            params.append(status)
        
        query += " ORDER BY f.id DESC"
        
        fines = execute_query(query, tuple(params), fetch_all=True)
        
        # Convert dates
        for fine in fines:
            if fine['issue_date']:
                fine['issue_date'] = fine['issue_date'].strftime('%Y-%m-%d')
            if fine['due_date']:
                fine['due_date'] = fine['due_date'].strftime('%Y-%m-%d')
            if fine['return_date']:
                fine['return_date'] = fine['return_date'].strftime('%Y-%m-%d')
            fine['fine_amount'] = float(fine['fine_amount'])
        
        return jsonify({'success': True, 'fines': fines}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@fines_bp.route('/<int:fine_id>', methods=['GET'])
def get_fine(fine_id):
    """Get single fine details"""
    try:
        query = """
            SELECT 
                f.*,
                l.issue_date,
                l.due_date,
                l.return_date,
                bd.title as book_title,
                m.name as member_name
            FROM Fines f
            JOIN Loans l ON f.loan_id = l.id
            JOIN Books b ON l.book_id = b.id
            JOIN BookDetails bd ON b.book_detail_id = bd.book_detail_id
            JOIN Members m ON l.member_id = m.id
            WHERE f.id = %s
        """
        fine = execute_query(query, (fine_id,), fetch_one=True)
        
        if fine:
            if fine['issue_date']:
                fine['issue_date'] = fine['issue_date'].strftime('%Y-%m-%d')
            if fine['due_date']:
                fine['due_date'] = fine['due_date'].strftime('%Y-%m-%d')
            if fine['return_date']:
                fine['return_date'] = fine['return_date'].strftime('%Y-%m-%d')
            fine['fine_amount'] = float(fine['fine_amount'])
            return jsonify({'success': True, 'fine': fine}), 200
        return jsonify({'error': 'Fine not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@fines_bp.route('/<int:fine_id>/pay', methods=['PUT'])
def pay_fine(fine_id):
    """Mark fine as paid"""
    try:
        query = "UPDATE Fines SET paid = 'paid' WHERE id = %s"
        execute_query(query, (fine_id,), commit=True)
        
        return jsonify({
            'success': True,
            'message': 'Fine marked as paid'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@fines_bp.route('/total', methods=['GET'])
def get_total_fines():
    """Get total unpaid fines"""
    try:
        query = """
            SELECT 
                SUM(fine_amount) as total_unpaid,
                COUNT(*) as count
            FROM Fines
            WHERE paid = 'unpaid'
        """
        result = execute_query(query, fetch_one=True)
        
        return jsonify({
            'success': True,
            'total_unpaid': float(result['total_unpaid'] or 0),
            'count': result['count']
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500