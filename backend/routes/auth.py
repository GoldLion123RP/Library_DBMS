from flask import Blueprint, request, jsonify
from database import execute_query

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return user details"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'Username and password required'}), 400
        
        # Check in AuthenticationSystem table
        query = """
            SELECT s.StaffID, s.FirstName, s.LastName, s.Username, s.Role, a.Password
            FROM Staff s
            JOIN AuthenticationSystem a ON s.StaffID = a.StaffID
            WHERE s.Username = %s
        """
        user = execute_query(query, (username,), fetch_one=True)
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Simple password check (in production, use hashing)
        if user['Password'] != password:
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Return user info (exclude password)
        return jsonify({
            'success': True,
            'user': {
                'id': user['StaffID'],
                'firstName': user['FirstName'],
                'lastName': user['LastName'],
                'username': user['Username'],
                'role': user['Role'],
                'token': f"token_{user['StaffID']}"  # Simple token
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/verify', methods=['GET'])
def verify_token():
    """Verify authentication token"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'No token provided'}), 401
        
        token = auth_header.replace('Bearer ', '')
        # Simple token validation (extract user ID)
        if token.startswith('token_'):
            user_id = int(token.replace('token_', ''))
            
            query = "SELECT StaffID, FirstName, LastName, Username, Role FROM Staff WHERE StaffID = %s"
            user = execute_query(query, (user_id,), fetch_one=True)
            
            if user:
                return jsonify({
                    'valid': True,
                    'user': {
                        'id': user['StaffID'],
                        'firstName': user['FirstName'],
                        'lastName': user['LastName'],
                        'username': user['Username'],
                        'role': user['Role']
                    }
                }), 200
        
        return jsonify({'error': 'Invalid token'}), 401
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500