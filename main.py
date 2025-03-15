from flask import Flask
from flask_restx import Api
from models import db
from flask_jwt_extended import JWTManager
from dashboard import dashboard_ns
from auth import auth_ns
from flask_cors import CORS
from datetime import timedelta

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    CORS(app, supports_credentials=True, origins=[app.config['ALLOWED_ORIGIN_1'], app.config['ALLOWED_ORIGIN_2'], app.config['ALLOWED_ORIGIN_3']])

    db.init_app(app)

    app.config["JWT_SECRET_KEY"] = app.config['MY_JWT_SECRET_KEY']
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=7)

    JWTManager(app)

    api = Api(app)

    api.add_namespace(dashboard_ns)
    api.add_namespace(auth_ns)
    return app