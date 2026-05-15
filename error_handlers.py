# ==================== ERROR HANDLERS ====================
"""
Centralized error handling for FERTILE MAP API
Provides consistent error responses across all endpoints
"""

from flask import jsonify, request
from marshmallow import ValidationError

class APIError(Exception):
    """Base API error class"""
    def __init__(self, message, status_code=400, payload=None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        """Convert error to dictionary"""
        rv = {
            'success': False,
            'error': self.message,
            'status_code': self.status_code
        }
        if self.payload:
            rv.update(self.payload)
        return rv

class ValidationAPIError(APIError):
    """Validation error"""
    def __init__(self, message, errors=None):
        super().__init__(message, 400, {'validation_errors': errors})

class AuthenticationError(APIError):
    """Authentication error"""
    def __init__(self, message='Authentication failed'):
        super().__init__(message, 401)

class AuthorizationError(APIError):
    """Authorization error"""
    def __init__(self, message='Access denied'):
        super().__init__(message, 403)

class NotFoundError(APIError):
    """Resource not found error"""
    def __init__(self, message='Resource not found'):
        super().__init__(message, 404)

class ConflictError(APIError):
    """Resource conflict error (e.g., duplicate)"""
    def __init__(self, message='Resource already exists'):
        super().__init__(message, 409)

class ServerError(APIError):
    """Server error"""
    def __init__(self, message='Internal server error'):
        super().__init__(message, 500)

def register_error_handlers(app, logger):
    """Register error handlers with Flask app"""
    
    @app.errorhandler(APIError)
    def handle_api_error(error):
        """Handle APIError exceptions"""
        logger.error(f"API Error: {error.message}", exc_info=error)
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """Handle Marshmallow validation errors"""
        logger.warning(f"Validation Error: {error.messages}")
        return jsonify({
            'success': False,
            'error': 'Validation failed',
            'validation_errors': error.messages,
            'status_code': 400
        }), 400
    
    @app.errorhandler(400)
    def handle_bad_request(error):
        """Handle 400 Bad Request"""
        logger.warning(f"Bad Request: {error}")
        return jsonify({
            'success': False,
            'error': 'Bad request',
            'status_code': 400
        }), 400
    
    @app.errorhandler(401)
    def handle_unauthorized(error):
        """Handle 401 Unauthorized"""
        logger.warning(f"Unauthorized: {error}")
        return jsonify({
            'success': False,
            'error': 'Unauthorized',
            'status_code': 401
        }), 401
    
    @app.errorhandler(403)
    def handle_forbidden(error):
        """Handle 403 Forbidden"""
        logger.warning(f"Forbidden: {error}")
        return jsonify({
            'success': False,
            'error': 'Access forbidden',
            'status_code': 403
        }), 403
    
    @app.errorhandler(404)
    def handle_not_found(error):
        """Handle 404 Not Found"""
        return jsonify({
            'success': False,
            'error': 'Resource not found',
            'status_code': 404
        }), 404
    
    @app.errorhandler(405)
    def handle_method_not_allowed(error):
        """Handle 405 Method Not Allowed"""
        return jsonify({
            'success': False,
            'error': 'Method not allowed',
            'status_code': 405
        }), 405
    
    @app.errorhandler(500)
    def handle_internal_error(error):
        """Handle 500 Internal Server Error"""
        logger.error(f"Internal Server Error: {error}", exc_info=error)
        return jsonify({
            'success': False,
            'error': 'Internal server error',
            'status_code': 500
        }), 500
    
    @app.errorhandler(Exception)
    def handle_unexpected_error(error):
        """Handle unexpected errors"""
        logger.error(f"Unexpected Error: {error}", exc_info=error)
        return jsonify({
            'success': False,
            'error': 'An unexpected error occurred',
            'status_code': 500
        }), 500

def create_success_response(data=None, message='Success', status_code=200):
    """Create standardized success response"""
    response = {
        'success': True,
        'message': message,
        'status_code': status_code
    }
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code

def create_error_response(error_message, status_code=400, errors=None):
    """Create standardized error response"""
    # Handle APIError objects
    if isinstance(error_message, APIError):
        error_msg = error_message.message
        status_code = error_message.status_code
    else:
        error_msg = str(error_message)
    
    response = {
        'success': False,
        'error': error_msg,
        'status_code': status_code
    }
    if errors:
        response['errors'] = errors
    return jsonify(response), status_code
