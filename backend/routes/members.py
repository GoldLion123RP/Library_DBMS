from flask import Blueprint, request, jsonify
from database import execute_query
from datetime import datetime

members_bp = Blueprint('members', __name__)

@members_bp.route('/', methods=['GET'])
def get_members():
    """Get all members"""
    try:
        search = request.args.get('search', '')
        active = request.args.get('active', '')
        
        query = "SELECT * FROM Members WHERE 1=1"
        params = []
        
        if search:
            query += " AND (name LIKE %s OR email LIKE %s OR membership_no LIKE %s)"
            search_param = f"%{search}%"
            params.extend([search_param, search_param, search_param])
        
        if active:
            query += " AND active = %s"
            params.append(1 if active == 'true' else 0)
        
        query += " ORDER BY name"
        
        members = execute_query(query, tuple(params), fetch_all=True)
        
        # Convert dates to strings
        for member in members:
            if member['join_date']:
                member['join_date'] = member['join_date'].strftime('%Y-%m-%d')
        
        return jsonify({'success': True, 'members': members}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@members_bp.route('/<int:member_id>', methods=['GET'])
def get_member(member_id):
    """Get single member details"""
    try:
        query = "SELECT * FROM Members WHERE id = %s"
        member = execute_query(query, (member_id,), fetch_one=True)
        
        if member:
            if member['join_date']:
                member['join_date'] = member['join_date'].strftime('%Y-%m-%d')
            return jsonify({'success': True, 'member': member}), 200
        return jsonify({'error': 'Member not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@members_bp.route('/', methods=['POST'])
def add_member():
    """Add new member"""
    try:
        data = request.get_json()
        
        query = """
            INSERT INTO Members (membership_no, name, email, phone, join_date, active)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        member_id = execute_query(query, (
            data['membership_no'],
            data['name'],
            data['email'],
            data['phone'],
            data.get('join_date', datetime.now().strftime('%Y-%m-%d')),
            data.get('active', 1)
        ), commit=True)
        
        return jsonify({
            'success': True,
            'message': 'Member added successfully',
            'member_id': member_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@members_bp.route('/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    """Update member details"""
    try:
        data = request.get_json()
        
        query = """
            UPDATE Members 
            SET name = %s, email = %s, phone = %s, active = %s
            WHERE id = %s
        """
        execute_query(query, (
            data['name'],
            data['email'],
            data['phone'],
            data.get('active', 1),
            member_id
        ), commit=True)
        
        return jsonify({'success': True, 'message': 'Member updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@members_bp.route('/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    """Delete member"""
    try:
        # Check if member has active loans
        query = "SELECT COUNT(*) as count FROM Loans WHERE member_id = %s AND status = 'issued'"
        result = execute_query(query, (member_id,), fetch_one=True)
        
        if result['count'] > 0:
            return jsonify({'error': 'Cannot delete member with active loans'}), 400
        
        query = "DELETE FROM Members WHERE id = %s"
        execute_query(query, (member_id,), commit=True)
        
        return jsonify({'success': True, 'message': 'Member deleted successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@members_bp.route('/<int:member_id>/history', methods=['GET'])
def get_member_history(member_id):
    """Get member's borrowing history"""
    try:
        query = """
            SELECT 
                l.id,
                l.issue_date,
                l.due_date,
                l.return_date,
                l.status,
                bd.title,
                bd.author,
                bd.isbn,
                CONCAT(u.FirstName, ' ', u.LastName) as issued_by
            FROM Loans l
            JOIN Books b ON l.book_id = b.id
            JOIN BookDetails bd ON b.book_detail_id = bd.book_detail_id
            JOIN Users u ON l.issued_by = u.id
            WHERE l.member_id = %s
            ORDER BY l.issue_date DESC
        """
        history = execute_query(query, (member_id,), fetch_all=True)
        
        # Convert dates to strings
        for record in history:
            if record['issue_date']:
                record['issue_date'] = record['issue_date'].strftime('%Y-%m-%d')
            if record['due_date']:
                record['due_date'] = record['due_date'].strftime('%Y-%m-%d')
            if record['return_date']:
                record['return_date'] = record['return_date'].strftime('%Y-%m-%d')
        
        return jsonify({'success': True, 'history': history}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500