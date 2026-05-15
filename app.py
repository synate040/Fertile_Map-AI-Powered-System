import os
import json
import jwt
import datetime
import logging
from functools import wraps
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from config import Config
from db import get_db, init_db
from models import db, User, SoilAnalysis
from validation import (
    user_schema, login_schema, analysis_schema, 
    validate_request_data
)
from logging_config import setup_logging
from error_handlers import (
    register_error_handlers, create_success_response, 
    create_error_response, APIError
)
from services.soil_analyzer import analyzer
from services.fertilizer import get_recommendations

app = Flask(__name__, static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '../Frontend')), static_url_path='')
app.config.from_object(Config)
CORS(app)
bcrypt = Bcrypt(app)

# Initialize SQLAlchemy ORM
db.init_app(app)

# Setup logging
logger = setup_logging(app)

# Register error handlers
register_error_handlers(app, logger)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

logger.info("FERTILE MAP application initialized successfully")


# ==================== AUTH MIDDLEWARE ====================
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get('Authorization', None)
        logger.info(f"[token_required] Authorization header: {auth_header}")
        
        if auth_header:
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
                logger.info(f"[token_required] Token extracted: {token[:20]}...")
            else:
                logger.warning(f"[token_required] Invalid authorization header format: {auth_header[:50]}")

        if not token:
            logger.warning("[token_required] No token provided")
            return create_error_response('Token is missing', 401)

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])

            if not current_user:
                return create_error_response('User not found', 401)

        except jwt.ExpiredSignatureError:
            return create_error_response('Token has expired', 401)
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token error: {str(e)}")
            return create_error_response('Invalid token', 401)
        except Exception as e:
            logger.error(f"Token validation error: {str(e)}")
            return create_error_response('Token validation failed', 401)

        return f(current_user, *args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return create_error_response('Token is missing', 401)

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])

            if not current_user:
                return create_error_response('User not found', 401)
            
            if current_user.role != 'admin':
                logger.warning(f"Unauthorized admin access attempt by user {current_user.id}")
                return create_error_response('Admin access required', 403)

        except jwt.ExpiredSignatureError:
            return create_error_response('Token has expired', 401)
        except jwt.InvalidTokenError as e:
            logger.warning(f"Invalid token error: {str(e)}")
            return create_error_response('Invalid token', 401)
        except Exception as e:
            logger.error(f"Token validation error: {str(e)}")
            return create_error_response('Token validation failed', 401)

        return f(current_user, *args, **kwargs)
    return decorated


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


# ==================== SERVE FRONTEND ====================
@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/pages/<path:filename>')
def serve_pages(filename):
    return send_from_directory(os.path.join(app.static_folder, 'pages'), filename)

@app.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory(os.path.join(app.static_folder, 'css'), filename)

@app.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory(os.path.join(app.static_folder, 'js'), filename)

# Serve favicon and other static assets
@app.route('/<path:filename>')
def serve_static(filename):
    if filename and '.' in filename:
        return send_from_directory(app.static_folder, filename)


# ==================== AUTH ROUTES ====================
@app.route('/api/auth/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        # Validate input using Marshmallow schema
        validated_data = validate_request_data(data, user_schema)
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=validated_data['email']).first()
        if existing_user:
            raise APIError('Email already registered', 409)
        
        # Hash password and create user
        password_hash = bcrypt.generate_password_hash(validated_data['password']).decode('utf-8')
        
        new_user = User(
            full_name=validated_data.get('full_name', ''),
            email=validated_data['email'],
            password_hash=password_hash,
            farm_name=validated_data.get('farm_name', ''),
            role=validated_data.get('role', 'user'),
            is_active=True
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        logger.info(f"New user registered: {new_user.email}")
        
        return create_success_response(
            new_user.to_dict(),
            "User registered successfully",
            201
        )
    except APIError as e:
        logger.warning(f"Registration failed: {str(e)}")
        return create_error_response(e, e.status_code)
    except Exception as e:
        logger.error(f"Unexpected error during registration: {str(e)}")
        return create_error_response(str(e), 500)


@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # Validate input using Marshmallow schema
        validated_data = validate_request_data(data, login_schema)
        
        # Find user by email
        user = User.query.filter_by(email=validated_data['email']).first()
        
        if not user or not bcrypt.check_password_hash(user.password_hash, validated_data['password']):
            logger.warning(f"Login failed for email: {validated_data['email']}")
            raise APIError('Invalid email or password', 401)
        
        if not user.is_active:
            logger.warning(f"Login attempt for inactive user: {validated_data['email']}")
            raise APIError('Account is inactive', 403)
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=30)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        
        logger.info(f"User logged in: {user.email}")
        logger.info(f"Generated token type: {type(token)}, length: {len(token) if token else 0}")
        logger.info(f"Token preview: {str(token)[:50]}..." if token else "Token is None or empty")
        
        response_data = {
            "token": token,
            "user": {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "farm_name": user.farm_name,
                "role": user.role
            }
        }
        logger.info(f"Login response structure: {response_data}")
        
        return create_success_response(response_data, "Login successful")
    except APIError as e:
        return create_error_response(e, e.status_code)
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        return create_error_response(str(e), 500)


@app.route('/api/auth/profile', methods=['GET'])
@token_required
def get_profile(current_user):
    return create_success_response(current_user.to_dict(), "Profile retrieved successfully")


@app.route('/api/auth/profile', methods=['PUT'])
@token_required
def update_profile(current_user):
    try:
        data = request.get_json()
        
        # Validate input
        from validation import update_user_schema
        validated_data = validate_request_data(data, update_user_schema)
        
        # Update user
        if 'full_name' in validated_data:
            current_user.full_name = validated_data['full_name']
        if 'farm_name' in validated_data:
            current_user.farm_name = validated_data['farm_name']
        
        db.session.commit()
        logger.info(f"User profile updated: {current_user.email}")
        
        return create_success_response(
            current_user.to_dict(),
            "Profile updated successfully"
        )
    except APIError as e:
        return create_error_response(e, e.status_code)
    except Exception as e:
        logger.error(f"Error updating profile: {str(e)}")
        db.session.rollback()
        return create_error_response(str(e), 500)


# ==================== ANALYSIS ROUTES ====================
@app.route('/api/analyze', methods=['POST'])
@token_required
def analyze_soil(current_user):
    try:
        # Check if image was uploaded
        if 'image' not in request.files:
            raise APIError('No image uploaded', 400)

        file = request.files['image']
        if file.filename == '':
            raise APIError('No file selected', 400)

        if not allowed_file(file.filename):
            raise APIError('File type not allowed. Use JPG, PNG, or WEBP', 400)

        # Save file
        filename = secure_filename(f"{current_user.id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        logger.info(f"File saved to: {filepath}")

        # Get crop type from form data
        crop_type = request.form.get('crop_type', 'general')

        # Run AI analysis
        logger.info(f"Starting analysis for file: {filepath}")
        prediction = analyzer.predict(filepath)
        logger.info(f"Analysis complete: {prediction.get('soil_type')}")
        
        # Get fertilizer recommendations
        recommendations = get_recommendations(prediction['soil_type'], crop_type)

        # Create new analysis record using ORM
        new_analysis = SoilAnalysis(
            user_id=current_user.id,
            image_url=filename,
            soil_type=prediction['soil_type'],
            confidence=prediction['confidence'],
            properties=prediction.get('properties', {}),
            predictions=prediction,
            recommendations=recommendations,
            selected_crop=crop_type,
            status='analyzed'
        )
        
        db.session.add(new_analysis)
        db.session.commit()
        
        logger.info(f"Soil analysis completed for user {current_user.id}: {prediction['soil_type']}")

        return create_success_response({
            "analysis_id": new_analysis.id,
            "soil_type": prediction['soil_type'],
            "confidence": round(prediction['confidence'], 2),
            "confidence_percent": f"{prediction['confidence']*100:.2f}",
            "properties": prediction.get('properties', {}),
            "recommendations": recommendations,
            "image_url": f"/api/uploads/{filename}"
        }, "Analysis completed", 200)
    except APIError as e:
        logger.error(f"API Error in analyze: {e.message}")
        return create_error_response(e, e.status_code)
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}", exc_info=True)
        db.session.rollback()
        return create_error_response(f"Analysis failed: {str(e)}", 500)


@app.route('/api/history', methods=['GET'])
@token_required
def get_history(current_user):
    try:
        # Get page and limit from query parameters
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        
        # Query analyses using ORM
        analyses_query = SoilAnalysis.query.filter_by(user_id=current_user.id).order_by(SoilAnalysis.created_at.desc())
        total = analyses_query.count()
        
        analyses = analyses_query.paginate(page=page, per_page=limit).items
        
        result = []
        for analysis in analyses:
            result.append({
                "id": analysis.id,
                "soil_type": analysis.soil_type,
                "confidence": round(analysis.confidence, 2),
                "properties": analysis.properties,
                "recommendations": analysis.recommendations,
                "crop_type": analysis.selected_crop,
                "image_url": f"/api/uploads/{analysis.image_url}",
                "created_at": analysis.created_at.isoformat()
            })
        
        return create_success_response({
            "analyses": result,
            "total": total,
            "page": page,
            "pages": (total + limit - 1) // limit
        }, "History retrieved successfully")
    except Exception as e:
        logger.error(f"Error retrieving history: {str(e)}")
        return create_error_response(str(e), 500)


@app.route('/api/history/<int:analysis_id>', methods=['DELETE'])
@token_required
def delete_analysis(current_user, analysis_id):
    try:
        # Find and verify ownership
        analysis = SoilAnalysis.query.get(analysis_id)
        
        if not analysis:
            raise APIError('Analysis not found', 404)
        
        if analysis.user_id != current_user.id:
            raise APIError('Unauthorized', 403)
        
        db.session.delete(analysis)
        db.session.commit()
        
        logger.info(f"Analysis {analysis_id} deleted by user {current_user.id}")
        
        return create_success_response(None, "Analysis deleted successfully")
    except APIError as e:
        return create_error_response(e, e.status_code)
    except Exception as e:
        logger.error(f"Error deleting analysis: {str(e)}")
        db.session.rollback()
        return create_error_response(str(e), 500)


@app.route('/api/uploads/<filename>')
def serve_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# ==================== ADMIN ROUTES ====================
@app.route('/api/admin/users', methods=['GET'])
@admin_required
def get_all_users(current_user):
    """Get all users (admin only)"""
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        
        users_query = User.query.order_by(User.created_at.desc())
        total = users_query.count()
        
        users = users_query.paginate(page=page, per_page=limit).items
        
        users_data = [
            {
                "id": u.id,
                "email": u.email,
                "full_name": u.full_name,
                "farm_name": u.farm_name,
                "role": u.role,
                "is_active": u.is_active,
                "created_at": u.created_at.isoformat()
            }
            for u in users
        ]
        
        return create_success_response({
            "users": users_data,
            "total": total,
            "page": page,
            "pages": (total + limit - 1) // limit
        }, "Users retrieved successfully")
    except Exception as e:
        logger.error(f"Error retrieving users: {str(e)}")
        return create_error_response(str(e), 500)


@app.route('/api/admin/users/<int:user_id>/role', methods=['PUT'])
@admin_required
def update_user_role(current_user, user_id):
    """Update user role (admin only)"""
    try:
        data = request.get_json()
        new_role = data.get('role', 'user')
        
        if new_role not in ['admin', 'user']:
            raise APIError("Invalid role. Must be 'admin' or 'user'", 400)
        
        user = User.query.get(user_id)
        if not user:
            raise APIError('User not found', 404)
        
        user.role = new_role
        db.session.commit()
        
        logger.info(f"User {user_id} role updated to {new_role} by admin {current_user.id}")
        
        return create_success_response(
            user.to_dict(),
            f"User role updated to {new_role}"
        )
    except APIError as e:
        return create_error_response(e, e.status_code)
    except Exception as e:
        logger.error(f"Error updating user role: {str(e)}")
        db.session.rollback()
        return create_error_response(str(e), 500)


@app.route('/api/admin/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(current_user, user_id):
    """Delete a user (admin only)"""
    try:
        if user_id == current_user.id:
            raise APIError("Cannot delete your own account", 400)
        
        user = User.query.get(user_id)
        if not user:
            raise APIError('User not found', 404)
        
        # Delete user (cascading delete will handle analyses)
        db.session.delete(user)
        db.session.commit()
        
        logger.warning(f"User {user_id} deleted by admin {current_user.id}")
        
        return create_success_response(None, f"User {user_id} deleted successfully")
    except APIError as e:
        return create_error_response(e, e.status_code)
    except Exception as e:
        logger.error(f"Error deleting user: {str(e)}")
        db.session.rollback()
        return create_error_response(str(e), 500)


@app.route('/api/admin/stats', methods=['GET'])
@admin_required
def get_admin_stats(current_user):
    """Get admin dashboard stats"""
    try:
        total_users = User.query.count()
        total_analyses = SoilAnalysis.query.count()
        admin_count = User.query.filter_by(role='admin').count()
        
        # Get soil type distribution
        from sqlalchemy import func
        soil_distribution = db.session.query(
            SoilAnalysis.soil_type,
            func.count(SoilAnalysis.id).label('count')
        ).group_by(SoilAnalysis.soil_type).all()
        
        return create_success_response({
            "total_users": total_users,
            "total_analyses": total_analyses,
            "admin_count": admin_count,
            "soil_distribution": [
                {"soil_type": s[0], "count": s[1]}
                for s in soil_distribution
            ]
        }, "Admin stats retrieved successfully")
    except Exception as e:
        logger.error(f"Error retrieving admin stats: {str(e)}")
        return create_error_response(str(e), 500)


# ==================== DATABASE MANAGEMENT ROUTES ====================
@app.route('/api/admin/database/info', methods=['GET'])
@admin_required
def get_database_info(current_user):
    """Get database information"""
    try:
        from sqlalchemy import inspect
        
        db_path = Config.SQLALCHEMY_DATABASE_URI.replace('sqlite:///', '')
        
        if not os.path.exists(db_path):
            raise APIError("Database file not found", 404)
        
        file_size = os.path.getsize(db_path)
        file_size_mb = round(file_size / (1024 * 1024), 2)
        
        # Get table information
        inspector = inspect(db.engine)
        table_names = inspector.get_table_names()
        
        tables_info = []
        for table_name in table_names:
            row_count = db.session.execute(db.text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
            tables_info.append({
                "name": table_name,
                "row_count": row_count
            })
        
        return create_success_response({
            "database_name": os.path.basename(db_path),
            "database_path": db_path,
            "file_size_bytes": file_size,
            "file_size_mb": file_size_mb,
            "total_users": User.query.count(),
            "total_analyses": SoilAnalysis.query.count(),
            "total_tables": len(tables_info),
            "tables": tables_info,
            "timestamp": datetime.datetime.now().isoformat()
        }, "Database info retrieved successfully")
    except APIError as e:
        return create_error_response(e, e.status_code)
    except Exception as e:
        logger.error(f"Error retrieving database info: {str(e)}")
        return create_error_response(str(e), 500)


@app.route('/api/admin/database/tables', methods=['GET'])
@admin_required
def get_database_tables(current_user):
    """Get all tables in database"""
    try:
        # Get table names using SQLAlchemy inspector
        from sqlalchemy import inspect
        
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        tables_info = []
        for table_name in tables:
            table_obj = db.Model.registry.mappers
            row_count = db.session.execute(db.text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
            tables_info.append({
                "name": table_name,
                "row_count": row_count
            })
        
        return create_success_response({
            "tables": tables_info,
            "total_tables": len(tables_info)
        }, "Tables retrieved successfully")
    except Exception as e:
        logger.error(f"Error retrieving tables: {str(e)}")
        return create_error_response(str(e), 500)


@app.route('/api/admin/database/table/<table_name>', methods=['GET'])
@admin_required
def get_table_data(current_user, table_name):
    """Get data from a specific table"""
    try:
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        
        # Validate table name - only allow alphanumeric and underscore
        if not table_name.replace('_', '').isalnum():
            raise APIError("Invalid table name", 400)
        
        from sqlalchemy import inspect, text
        
        inspector = inspect(db.engine)
        
        if table_name not in inspector.get_table_names():
            raise APIError("Table not found", 404)
        
        # Get column names
        columns = [col['name'] for col in inspector.get_columns(table_name)]
        
        # Query table data
        query_result = db.session.execute(
            text(f"SELECT * FROM {table_name} LIMIT {limit} OFFSET {(page - 1) * limit}")
        )
        
        total = db.session.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar()
        
        rows = []
        for row in query_result:
            rows.append(dict(row._mapping))
        
        return create_success_response({
            "table": table_name,
            "columns": columns,
            "rows": rows,
            "total": total,
            "page": page,
            "pages": (total + limit - 1) // limit
        }, "Table data retrieved successfully")
    except APIError as e:
        return create_error_response(e, e.status_code)
    except Exception as e:
        logger.error(f"Error retrieving table data: {str(e)}")
        return create_error_response(str(e), 500)


@app.route('/api/admin/database/table/<table_name>/schema', methods=['GET'])
@admin_required
def get_table_schema(current_user, table_name):
    """Get schema of a specific table"""
    try:
        if not table_name.replace('_', '').isalnum():
            raise APIError("Invalid table name", 400)
        
        from sqlalchemy import inspect
        
        inspector = inspect(db.engine)
        
        if table_name not in inspector.get_table_names():
            raise APIError("Table not found", 404)
        
        columns_info = inspector.get_columns(table_name)
        pk_constraint = inspector.get_pk_constraint(table_name)
        
        schema = []
        for col in columns_info:
            schema.append({
                "name": col['name'],
                "type": str(col['type']),
                "nullable": col['nullable'],
                "is_primary_key": col['name'] in pk_constraint.get('constrained_columns', [])
            })
        
        return create_success_response({
            "table": table_name,
            "schema": schema
        }, "Schema retrieved successfully")
    except APIError as e:
        return create_error_response(e, e.status_code)
    except Exception as e:
        logger.error(f"Error retrieving table schema: {str(e)}")
        return create_error_response(str(e), 500)


# ==================== EDUCATION ROUTES ====================
@app.route('/api/education/soil-types', methods=['GET'])
def get_soil_education():
    content = {
        "loamy": {
            "title": "Loamy Soil",
            "description": "Loamy soil is considered the gold standard for agriculture. It's a balanced mixture of sand, silt, and clay particles, providing excellent drainage while retaining adequate moisture and nutrients.",
            "composition": {"sand": 40, "silt": 40, "clay": 20},
            "best_crops": ["Wheat", "Corn", "Tomatoes", "Peppers", "Most vegetables", "Fruit trees"],
            "characteristics": [
                "Dark brown color",
                "Crumbly texture",
                "Holds moisture well",
                "Rich in nutrients",
                "Easy to work with"
            ]
        },
        "sandy": {
            "title": "Sandy Soil",
            "description": "Sandy soil has large particles with lots of air space. It drains quickly but doesn't retain nutrients well. Best for root vegetables and drought-tolerant plants.",
            "composition": {"sand": 70, "silt": 15, "clay": 15},
            "best_crops": ["Carrots", "Potatoes", "Lettuce", "Strawberries", "Herbs"],
            "characteristics": [
                "Light brown/tan color",
                "Gritty texture",
                "Drains very quickly",
                "Warms up fast in spring",
                "Low nutrient retention"
            ]
        },
        "clay": {
            "title": "Clay Soil",
            "description": "Clay soil has very fine particles that pack tightly together. It retains water and nutrients well but can become waterlogged and is difficult to work when wet.",
            "composition": {"sand": 20, "silt": 20, "clay": 60},
            "best_crops": ["Rice", "Wheat", "Broccoli", "Cabbage", "Beans"],
            "characteristics": [
                "Red/brown/grey color",
                "Sticky when wet",
                "Hard when dry",
                "Excellent nutrient retention",
                "Poor drainage"
            ]
        },
        "silty": {
            "title": "Silty Soil",
            "description": "Silty soil has medium-sized particles with a smooth, flour-like feel. It's fertile and retains moisture well but is prone to compaction and erosion.",
            "composition": {"sand": 20, "silt": 60, "clay": 20},
            "best_crops": ["Most vegetables", "Grasses", "Wetland crops", "Shrubs"],
            "characteristics": [
                "Dark brown color",
                "Silky smooth texture",
                "Holds moisture well",
                "Fertile",
                "Prone to erosion"
            ]
        },
        "peaty": {
            "title": "Peaty Soil",
            "description": "Peaty soil is rich in organic matter and usually found in marshy areas. It's very acidic and retains a lot of water. Excellent for acid-loving plants.",
            "composition": {"organic_matter": 70, "mineral": 30},
            "best_crops": ["Blueberries", "Potatoes", "Lantern plants", "Witch hazel", "Heather"],
            "characteristics": [
                "Very dark/black color",
                "Spongy texture",
                "Highly acidic",
                "Waterlogged naturally",
                "Rich in organic matter"
            ]
        },
        "chalky": {
            "title": "Chalky Soil",
            "description": "Chalky soil overlies limestone or chalk bedrock. It's alkaline, stony, and can cause nutrient lockout, especially iron and manganese deficiency.",
            "composition": {"calcium_carbonate": 40, "sand": 30, "clay": 30},
            "best_crops": ["Lavender", "Lilac", "Spinach", "Beets", "Sweet corn"],
            "characteristics": [
                "Pale/white color",
                "Stony, gritty texture",
                "Very alkaline (high pH)",
                "Free-draining",
                "Can cause yellowing in plants"
            ]
        }
    }
    return jsonify(content)


@app.route('/api/education/fertilizer-guide', methods=['GET'])
def get_fertilizer_guide():
    guide = {
        "npk_explained": {
            "title": "Understanding N-P-K Ratios",
            "content": "Every fertilizer bag shows three numbers (e.g., 10-20-10). These represent the percentage of Nitrogen (N), Phosphorus (P), and Potassium (K).",
            "details": {
                "nitrogen": {
                    "symbol": "N",
                    "role": "Promotes leaf and stem growth, green color",
                    "deficiency_signs": "Yellowing of older leaves, stunted growth",
                    "excess_signs": "Excessive foliage, weak stems, delayed flowering"
                },
                "phosphorus": {
                    "symbol": "P",
                    "role": "Root development, flowering, fruiting",
                    "deficiency_signs": "Purple/red leaves, poor root growth",
                    "excess_signs": "Blocks uptake of zinc and iron"
                },
                "potassium": {
                    "symbol": "K",
                    "role": "Overall plant health, disease resistance, water regulation",
                    "deficiency_signs": "Brown leaf edges, weak stems",
                    "excess_signs": "Blocks calcium and magnesium uptake"
                }
            }
        },
        "application_methods": {
            "title": "How to Apply Fertilizers",
            "methods": [
                {
                    "name": "Broadcasting",
                    "description": "Spread evenly across the entire field",
                    "best_for": "Pre-planting, large areas"
                },
                {
                    "name": "Banding",
                    "description": "Place fertilizer in bands near seed rows",
                    "best_for": "Row crops, efficient nutrient use"
                },
                {
                    "name": "Side-dressing",
                    "description": "Apply alongside growing plants",
                    "best_for": "Mid-season nutrient boost"
                },
                {
                    "name": "Foliar Spray",
                    "description": "Spray liquid fertilizer on leaves",
                    "best_for": "Quick nutrient deficiency fix"
                }
            ]
        },
        "organic_vs_synthetic": {
            "title": "Organic vs Synthetic Fertilizers",
            "organic": {
                "pros": ["Improves soil structure", "Slow release", "Environmentally friendly", "Builds soil biology"],
                "cons": ["Slower results", "Variable nutrient content", "Bulky to transport", "More expensive per nutrient"]
            },
            "synthetic": {
                "pros": ["Fast acting", "Precise nutrient ratios", "Cost-effective", "Easy to apply"],
                "cons": ["Can burn plants", "Degrades soil over time", "Environmental runoff risk", "Doesn't improve soil structure"]
            }
        }
    }
    return jsonify(guide)


# ==================== STATS ROUTE ====================
@app.route('/api/stats', methods=['GET'])
@token_required
def get_stats(current_user):
    db = get_db()

    total = db.execute(
        'SELECT COUNT(*) as count FROM analyses WHERE user_id = ?',
        (current_user['id'],)
    ).fetchone()['count']

    soil_distribution = db.execute(
        '''SELECT soil_type, COUNT(*) as count 
           FROM analyses WHERE user_id = ? 
           GROUP BY soil_type''',
        (current_user['id'],)
    ).fetchall()

    recent = db.execute(
        '''SELECT soil_type, confidence, created_at 
           FROM analyses WHERE user_id = ? 
           ORDER BY created_at DESC LIMIT 10''',
        (current_user['id'],)
    ).fetchall()

    avg_confidence = db.execute(
        'SELECT AVG(confidence) as avg FROM analyses WHERE user_id = ?',
        (current_user['id'],)
    ).fetchone()['avg']

    db.close()

    return jsonify({
        "total_analyses": total,
        "average_confidence": round(avg_confidence or 0, 2),
        "soil_distribution": [
            {"soil_type": s['soil_type'], "count": s['count']}
            for s in soil_distribution
        ],
        "recent_analyses": [
            {
                "soil_type": r['soil_type'],
                "confidence": r['confidence'],
                "date": r['created_at']
            }
            for r in recent
        ]
    })


# ==================== RUN SERVER ====================
if __name__ == '__main__':
    with app.app_context():
        # Initialize database with SQLAlchemy ORM
        db.create_all()
        logger.info("Database tables created/verified")
        
        # Create admin user if it doesn't exist
        admin = User.query.filter_by(email='admin@fertilemap.com').first()
        if not admin:
            try:
                password_hash = bcrypt.generate_password_hash('Admin@123').decode('utf-8')
                admin_user = User(
                    email='admin@fertilemap.com',
                    password_hash=password_hash,
                    full_name='Admin User',
                    farm_name='Main Farm',
                    role='admin',
                    is_active=True
                )
                db.session.add(admin_user)
                db.session.commit()
                logger.info("✅ Admin user created: admin@fertilemap.com / Admin@123")
                print("\n" + "=" * 70)
                print("✅ ADMIN USER CREATED")
                print("=" * 70)
                print("\n📧 Email:    admin@fertilemap.com")
                print("🔐 Password: Admin@123")
                print("\n" + "=" * 70 + "\n")
            except Exception as e:
                logger.error(f"Error creating admin user: {e}")
        
    app.run(debug=True, port=5000)
