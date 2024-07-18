from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_wtf.csrf import CSRFProtect
from flask_smorest import Api

migrate = Migrate()
jwt = JWTManager()
cors = CORS()
csrf = CSRFProtect()
ma = Marshmallow()
api = Api()
