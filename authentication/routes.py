from flask import Blueprint

from .views import (
    UserLoginView,
    UserRegisterView,
    UserRefreshView,
    ProtectedView,
)

blueprint = Blueprint(
    "authentication",
    __name__,
    url_prefix="/authentication",
)

blueprint.add_url_rule(
    "/register",
    view_func=UserRegisterView.as_view("register"),
)

blueprint.add_url_rule(
    "/login",
    view_func=UserLoginView.as_view("login"),
)

blueprint.add_url_rule(
    "/refresh",
    view_func=UserRefreshView.as_view("refresh"),
)

blueprint.add_url_rule(
    "/protected",
    view_func=ProtectedView.as_view("protected"),
)
