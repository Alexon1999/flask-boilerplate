from flask import request, jsonify, current_app as app
from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from .models import User
from configs import db
from .schemas import user_schema, user_register_schema, user_login_schema


class UserRegisterView(MethodView):
    def post(self):
        data = request.get_json()
        errors = user_register_schema.validate(data)
        if errors:
            return jsonify(errors), 400

        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        if (
            User.query.filter_by(username=username).first()
            or User.query.filter_by(email=email).first()
        ):
            app.logger.error(f"User already exists")
            return jsonify({"message": "User already exists"}), 400

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        app.logger.info(f"User {username} created successfully")

        return user_schema.jsonify(new_user), 201


class UserLoginView(MethodView):
    def post(self):
        data = request.get_json()
        errors = user_login_schema.validate(data)
        if errors:
            return jsonify(errors), 400

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

        return jsonify({"message": "Invalid credentials"}), 401


class UserRefreshView(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user, fresh=False)
        return jsonify(access_token=access_token), 200


class ProtectedView(MethodView):
    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return jsonify(logged_in_as=current_user), 200
