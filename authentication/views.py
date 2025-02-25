from flask import jsonify, current_app as app
from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    jwt_required,
    get_jwt_identity,
)
from flask_smorest import Blueprint, abort
from injector import inject

from authentication.utils import user_required
from .services import UserService
from .schemas import (
    user_schema,
    users_schema,
    user_query_args_schema,
    user_register_schema,
    user_update_schema,
    user_login_schema,
    jwt_token_pair_schema,
    jwt_token_after_refresh_schema,
)


# Create a blueprint for the authentication API, you can have nested blueprints (blp.register_blueprint(nested_blp))
blp = Blueprint(
    "authentication",
    __name__,
    url_prefix="/authentication",
    description="Authentication API",
)


@blp.route("/user/register")
class UserRegisterView(MethodView):

    @inject
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    @blp.arguments(schema=user_register_schema)
    @blp.response(status_code=201, schema=user_schema)
    def post(self, data):
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        try:
            new_user = self.user_service.create_user(username, email, password)
            app.logger.info(f"User {username} created successfully")
            return new_user
        except ValueError as e:
            app.logger.error(str(e))
            abort(400, message=str(e))


@blp.route("/login")
class UserLoginView(MethodView):

    @inject
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    @blp.arguments(schema=user_login_schema)
    @blp.response(status_code=200, schema=jwt_token_pair_schema)
    def post(self, data):
        email = data.get("email")
        password = data.get("password")

        try:
            user = self.user_service.authenticate_user(email, password)
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }, 200
        except ValueError as e:
            app.logger.error(str(e))
            abort(401, message=str(e))


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
        print(get_jwt())
        print(get_jwt_identity())
        current_user = get_jwt_identity()
        return jsonify(logged_in_as=current_user), 200


@blp.route("/users")
class UsersView(MethodView):
    @inject
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    @jwt_required()
    @blp.arguments(user_query_args_schema, location="query")
    @blp.response(status_code=200, schema=users_schema)
    def get(self, params):
        users = self.user_service.list_users(params)
        return users


@blp.route("/users/<int:user_id>")
class UserView(MethodView):
    @inject
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    @jwt_required()
    @user_required
    @blp.response(status_code=200, schema=user_schema)
    def get(self, user_id):
        try:
            user = self.user_service.get_user_by_id(user_id)
            return user
        except ValueError as e:
            app.logger.error(str(e))
            abort(404, message=str(e))

    @jwt_required()
    @user_required
    @blp.arguments(schema=user_update_schema)
    @blp.response(status_code=200, schema=user_schema)
    def put(self, data, user_id):
        username = data.get("username")
        password = data.get("password")

        try:
            user = self.user_service.update_user(user_id, username, password)
            return user
        except ValueError as e:
            app.logger.error(str(e))
            abort(400, message=str(e))

    @jwt_required()
    @user_required
    @blp.response(status_code=204)
    def delete(self, user_id):
        try:
            user = self.user_service.get_user_by_id(user_id)
            self.user_service.delete_user(user)
        except ValueError as e:
            app.logger.error(str(e))
            abort(404, message=str(e))
