# ==================== VALIDATION SCHEMAS ====================
"""
Data validation schemas using Marshmallow
Validates request data before processing
"""

from marshmallow import Schema, fields, validate, ValidationError, post_load
from email_validator import validate_email, EmailNotValidError

class UserSchema(Schema):
    """User registration and profile schema"""
    id = fields.Int(dump_only=True)
    full_name = fields.Str(
        required=True,
        validate=validate.Length(min=2, max=255),
        error_messages={'required': 'Full name is required'}
    )
    email = fields.Email(
        required=True,
        error_messages={'required': 'Email is required', 'invalid': 'Invalid email format'}
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=6, max=255),
        load_only=True,
        error_messages={'required': 'Password is required', 'validator_failed': 'Password must be at least 6 characters'}
    )
    farm_name = fields.Str(validate=validate.Length(max=255), allow_none=True)
    role = fields.Str(validate=validate.OneOf(['user', 'admin']), dump_only=True)
    is_active = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    
    class Meta:
        fields = ('id', 'full_name', 'email', 'password', 'farm_name', 'role', 'is_active', 'created_at')

class LoginSchema(Schema):
    """User login schema"""
    email = fields.Email(
        required=True,
        error_messages={'required': 'Email is required', 'invalid': 'Invalid email format'}
    )
    password = fields.Str(
        required=True,
        validate=validate.Length(min=6),
        error_messages={'required': 'Password is required'}
    )

class SoilAnalysisSchema(Schema):
    """Soil analysis schema"""
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    image_url = fields.Str(allow_none=True)
    soil_type = fields.Str(
        required=True,
        validate=validate.OneOf(['loamy', 'sandy', 'clay', 'silty', 'peaty', 'chalky']),
        error_messages={'required': 'Soil type is required'}
    )
    confidence = fields.Float(
        validate=validate.Range(min=0, max=100),
        allow_none=True
    )
    properties = fields.Dict(allow_none=True)
    predictions = fields.Dict(allow_none=True)
    recommendations = fields.Dict(allow_none=True)
    selected_crop = fields.Str(validate=validate.Length(max=100), allow_none=True)
    status = fields.Str(validate=validate.OneOf(['pending', 'analyzed', 'archived']))
    created_at = fields.DateTime(dump_only=True)
    
    class Meta:
        fields = ('id', 'user_id', 'image_url', 'soil_type', 'confidence', 
                  'properties', 'predictions', 'recommendations', 'selected_crop', 'status', 'created_at')

class UpdateUserSchema(Schema):
    """Schema for updating user profile"""
    full_name = fields.Str(validate=validate.Length(min=2, max=255), allow_none=True)
    farm_name = fields.Str(validate=validate.Length(max=255), allow_none=True)

class ChangePasswordSchema(Schema):
    """Schema for changing password"""
    current_password = fields.Str(
        required=True,
        validate=validate.Length(min=6),
        error_messages={'required': 'Current password is required'}
    )
    new_password = fields.Str(
        required=True,
        validate=validate.Length(min=6),
        error_messages={'required': 'New password is required', 'validator_failed': 'Password must be at least 6 characters'}
    )
    confirm_password = fields.Str(
        required=True,
        error_messages={'required': 'Password confirmation is required'}
    )

# Create schema instances
user_schema = UserSchema()
users_schema = UserSchema(many=True)
login_schema = LoginSchema()
analysis_schema = SoilAnalysisSchema()
analyses_schema = SoilAnalysisSchema(many=True)
update_user_schema = UpdateUserSchema()
change_password_schema = ChangePasswordSchema()

def validate_request_data(data, schema):
    """
    Validate request data against schema
    Returns validated data or raises ValidationError
    """
    try:
        return schema.load(data)
    except ValidationError as err:
        raise err
