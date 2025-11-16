from functools import wraps
from flask import request, jsonify

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'Authentication required'}), 401
        
        # Simple token validation (you can enhance this with JWT)
        token = auth_header.replace('Bearer ', '')
        if not token:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # You can add role validation here
        return f(*args, **kwargs)
    return decorated_function

def format_date(date):
    """Format date for display"""
    if date:
        return date.strftime('%Y-%m-%d')
    return None

def calculate_fine(due_date, return_date, rate_per_day=5):
    """Calculate fine amount"""
    if return_date and return_date > due_date:
        days_late = (return_date - due_date).days
        return days_late * rate_per_day
    return 0