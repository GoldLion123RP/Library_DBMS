 
from flask import Blueprint, request, jsonify
from database import execute_query, get_db_connection

staff_bp = Blueprint('staff', __name__)

@staff_bp.route('/', methods=['GET'])
def get_all_staff():
    """Get all staff members (Admin only)"""
    try:
        query = """
            SELECT 
                s.StaffID,
                s.FirstName,
                s.LastName,
                s.Username,
                s.Role
            FROM Staff s
            ORDER BY s.StaffID
        """
        staff = execute_query(query, fetch_all=True)
        
        return jsonify({'success': True, 'staff': staff}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@staff_bp.route('/<int:staff_id>', methods=['GET'])
def get_staff(staff_id):
    """Get single staff member details"""
    try:
        query = """
            SELECT 
                s.StaffID,
                s.FirstName,
                s.LastName,
                s.Username,
                s.Role
            FROM Staff s
            WHERE s.StaffID = %s
        """
        staff = execute_query(query, (staff_id,), fetch_one=True)
        
        if staff:
            return jsonify({'success': True, 'staff': staff}), 200
        return jsonify({'error': 'Staff not found'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@staff_bp.route('/', methods=['POST'])
def add_staff():
    """Add new staff member (Admin only)"""
    try:
        data = request.get_json()
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Insert into Staff table
        cursor.execute("""
            INSERT INTO Staff (FirstName, LastName, Username, PasswordHash, Role)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data['firstName'],
            data['lastName'],
            data['username'],
            'hashed',  # In production, use proper password hashing
            data['role']
        ))
        
        staff_id = cursor.lastrowid
        
        # Insert into AuthenticationSystem
        cursor.execute("""
            INSERT INTO AuthenticationSystem (StaffID, Password)
            VALUES (%s, %s)
        """, (staff_id, data['password']))
        
        # Also add to Users table for consistency
        cursor.execute("""
            INSERT INTO Users (FirstName, LastName, email, password, phone, full_name, role_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data['firstName'],
            data['lastName'],
            data.get('email', ''),
            data['password'],
            data.get('phone', ''),
            f"{data['firstName']} {data['lastName']}",
            1 if data['role'] == 'Admin' else (2 if data['role'] == 'Librarian' else 3)
        ))
        
        connection.commit()
        connection.close()
        
        return jsonify({
            'success': True,
            'message': 'Staff member added successfully',
            'staff_id': staff_id
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@staff_bp.route('/<int:staff_id>', methods=['PUT'])
def update_staff(staff_id):
    """Update staff member (Admin only)"""
    try:
        data = request.get_json()
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Update Staff table
        cursor.execute("""
            UPDATE Staff 
            SET FirstName = %s, LastName = %s, Username = %s, Role = %s
            WHERE StaffID = %s
        """, (
            data['firstName'],
            data['lastName'],
            data['username'],
            data['role'],
            staff_id
        ))
        
        # Update password if provided
        if data.get('password'):
            cursor.execute("""
                UPDATE AuthenticationSystem 
                SET Password = %s
                WHERE StaffID = %s
            """, (data['password'], staff_id))
        
        connection.commit()
        connection.close()
        
        return jsonify({
            'success': True,
            'message': 'Staff member updated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@staff_bp.route('/<int:staff_id>', methods=['DELETE'])
def delete_staff(staff_id):
    """Delete staff member (Admin only)"""
    try:
        # Prevent deleting if staff has issued books
        result = execute_query("""
            SELECT COUNT(*) as count FROM Loans WHERE issued_by = %s
        """, (staff_id,), fetch_one=True)
        
        if result['count'] > 0:
            return jsonify({
                'error': 'Cannot delete staff member who has issued books'
            }), 400
        
        connection = get_db_connection()
        cursor = connection.cursor()
        
        # Delete from AuthenticationSystem
        cursor.execute("DELETE FROM AuthenticationSystem WHERE StaffID = %s", (staff_id,))
        
        # Delete from Staff
        cursor.execute("DELETE FROM Staff WHERE StaffID = %s", (staff_id,))
        
        connection.commit()
        connection.close()
        
        return jsonify({
            'success': True,
            'message': 'Staff member deleted successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500