from functools import wraps
from flask_jwt_extended import get_jwt_identity
from flask_smorest import abort


def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_id = kwargs.get("user_id")
        current_user_id = get_jwt_identity()
        if current_user_id != user_id:
            abort(
                403, message="You are not authorized to perform this action."
            )
        return f(*args, **kwargs)

    return decorated_function
