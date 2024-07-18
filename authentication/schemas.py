from configs import ma
from .models import User
from marshmallow import fields, validate


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ("_password_hash",)


class UserRegisterSchema(ma.Schema):
    username = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))


class UserLoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))


class JWTTokenPairSchema(ma.Schema):
    access_token = fields.Str()
    refresh_token = fields.Str()


class JWTTokenAfterRefreshSchema(ma.Schema):
    access_token = fields.Str(required=True)


# Create instances of the schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
user_register_schema = UserRegisterSchema()
user_login_schema = UserLoginSchema()
jwt_token_pair_schema = JWTTokenPairSchema()
jwt_token_after_refresh_schema = JWTTokenAfterRefreshSchema()
