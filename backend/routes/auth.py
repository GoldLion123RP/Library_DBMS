from flask import Blueprint, request, jsonify
from database import execute_query, get_db_connection
from datetime import datetime

auth_bp = Blueprint('auth', __name__)

def log_login_attempt(username, status, staff_id=None, failure_reason=None):
    """Log login attempt to audit table"""
    try:
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent', 'Unknown')
        
        query = """
            INSERT INTO LoginAuditLog 
            (username, login_status, ip_address, user_agent, staff_id, failure_reason)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        execute_query(query, (
            username,
            status,
            ip_address,
            user_agent,
            staff_id,
            failure_reason
        ), commit=True)
    except Exception as e:
        print(f"Error logging login attempt: {e}")

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and return user details"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            log_login_attempt(username or 'unknown', 'failed', failure_reason='Missing credentials')
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
            log_login_attempt(username, 'failed', failure_reason='User not found')
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Simple password check (in production, use hashing)
        if user['Password'] != password:
            log_login_attempt(username, 'failed', staff_id=user['StaffID'], failure_reason='Incorrect password')
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Successful login
        log_login_attempt(username, 'success', staff_id=user['StaffID'])
        
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
        log_login_attempt(username if 'username' in locals() else 'unknown', 'failed', failure_reason=f'System error: {str(e)}')
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

@auth_bp.route('/login-logs', methods=['GET'])
def get_login_logs():
    """Get login audit logs (Admin only)"""
    try:
        # Optional filters
        username_filter = request.args.get('username', '')
        status_filter = request.args.get('status', '')
        limit = int(request.args.get('limit', 100))
        
        query = """
            SELECT 
                log_id,
                username,
                login_attempt_time,
                login_status,
                ip_address,
                user_agent,
                staff_id,
                failure_reason,
                CONCAT(s.FirstName, ' ', s.LastName) as full_name
            FROM LoginAuditLog l
            LEFT JOIN Staff s ON l.staff_id = s.StaffID
            WHERE 1=1
        """
        params = []
        
        if username_filter:
            query += " AND username LIKE %s"
            params.append(f"%{username_filter}%")
        
        if status_filter:
            query += " AND login_status = %s"
            params.append(status_filter)
        
        query += " ORDER BY login_attempt_time DESC LIMIT %s"
        params.append(limit)
        
        logs = execute_query(query, tuple(params), fetch_all=True)
        
        # Format datetime
        for log in logs:
            if log['login_attempt_time']:
                log['login_attempt_time'] = log['login_attempt_time'].strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify({'success': True, 'logs': logs}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login-stats', methods=['GET'])
def get_login_stats():
    """Get login statistics (Admin only)"""
    try:
        stats = {}
        
        # Total logins today
        query = """
            SELECT COUNT(*) as count 
            FROM LoginAuditLog 
            WHERE DATE(login_attempt_time) = CURDATE()
        """
        result = execute_query(query, fetch_one=True)
        stats['today_logins'] = result['count']
        
        # Failed logins today
        query = """
            SELECT COUNT(*) as count 
            FROM LoginAuditLog 
            WHERE DATE(login_attempt_time) = CURDATE() AND login_status = 'failed'
        """
        result = execute_query(query, fetch_one=True)
        stats['today_failed'] = result['count']
        
        # Most active users (last 7 days)
        query = """
            SELECT username, COUNT(*) as login_count
            FROM LoginAuditLog
            WHERE login_attempt_time >= DATE_SUB(NOW(), INTERVAL 7 DAY)
            AND login_status = 'success'
            GROUP BY username
            ORDER BY login_count DESC
            LIMIT 5
        """
        stats['top_users'] = execute_query(query, fetch_all=True) or []
        
        # Recent failed attempts
        query = """
            SELECT username, COUNT(*) as fail_count
            FROM LoginAuditLog
            WHERE login_attempt_time >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
            AND login_status = 'failed'
            GROUP BY username
            ORDER BY fail_count DESC
            LIMIT 5
        """
        stats['failed_attempts'] = execute_query(query, fetch_all=True) or []
        
        return jsonify({'success': True, 'stats': stats}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500