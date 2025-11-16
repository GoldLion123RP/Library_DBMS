from flask import Flask, jsonify
from flask_cors import CORS
from config import Config

# Import route blueprints
from routes.auth import auth_bp
from routes.books import books_bp
from routes.members import members_bp
from routes.loans import loans_bp
from routes.fines import fines_bp
from routes.reports import reports_bp
from routes.staff import staff_bp

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS with proper configuration
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Disable strict slashes to prevent redirects
app.url_map.strict_slashes = False

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(books_bp, url_prefix='/api/books')
app.register_blueprint(members_bp, url_prefix='/api/members')
app.register_blueprint(loans_bp, url_prefix='/api/loans')
app.register_blueprint(fines_bp, url_prefix='/api/fines')
app.register_blueprint(reports_bp, url_prefix='/api/reports')
app.register_blueprint(staff_bp, url_prefix='/api/staff')

# Root endpoint
@app.route('/')
def home():
    return jsonify({
        'message': 'Library Management System API',
        'version': '1.0.0',
        'status': 'running',
        'endpoints': {
            'auth': '/api/auth',
            'books': '/api/books',
            'members': '/api/members',
            'loans': '/api/loans',
            'fines': '/api/fines',
            'reports': '/api/reports',
            'staff': '/api/staff'
        }
    })

# Health check endpoint
@app.route('/health')
def health():
    return jsonify({'status': 'healthy'}), 200

# Handle OPTIONS requests for CORS preflight
@app.route('/api/<path:path>', methods=['OPTIONS'])
def options_handler(path):
    return '', 204

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=Config.DEBUG
    )
    