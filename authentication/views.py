from flask import jsonify, current_app as app
from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from flask_smorest import Blueprint, abort
from .models import User
from configs import db
from .schemas import (
    user_schema,
    user_register_schema,
    user_login_schema,
    jwt_token_pair_schema,
    jwt_token_after_refresh_schema,
)


# Create a blueprint for the authentication API
blp = Blueprint(
    "authentication",
    __name__,
    url_prefix="/authentication",
    description="Authentication API",
)


@blp.route("/registers")
class UserRegisterView(MethodView):

    @blp.arguments(schema=user_register_schema)
    @blp.response(status_code=201, schema=user_schema)
    def post(self, data):
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if (
            User.query.filter_by(username=username).first()
            or User.query.filter_by(email=email).first()
        ):
            app.logger.error(f"User already exists")
            abort(400, message="User already exists")

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        app.logger.info(f"User {username} created successfully")

        return new_user


@blp.route("/login")
class UserLoginView(MethodView):
    @blp.arguments(schema=user_login_schema)
    @blp.response(status_code=200, schema=jwt_token_pair_schema)
    def post(self, data):
        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            access_token = create_access_token(
                identity=user.id,
            )
            refresh_token = create_refresh_token(
                identity=user.id,
            )
            return (
                jsonify(
                    access_token=access_token, refresh_token=refresh_token
                ),
                200,
            )

        return abort(401, message="Invalid email or password")


@blp.route("/refresh")
class UserRefreshView(MethodView):
    @jwt_required(refresh=True)
    @blp.response(status_code=200, schema=jwt_token_after_refresh_schema)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user, fresh=False)
        return jsonify(access_token=access_token), 200


@blp.route("/protected")
class ProtectedView(MethodView):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return jsonify(logged_in_as=current_user), 200
