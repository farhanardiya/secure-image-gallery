from flask import Flask, Blueprint
from flask_restx import Api
from flask_jwt_extended import JWTManager
from .extensions import db

from .api import root
from .api.register import api as register_api
from .api.login import api as login_api
from .api.image import api as image_api

def register_blueprint(app):
    bp = Blueprint("API", __name__, url_prefix="/api/v1")

    authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}

    api = Api(
        bp,
        version="1.0",
        title="Secure Gallery Backend API",
        description="Welcome to the Swagger Secure Gallery!",
        doc="/doc",
        authorizations=authorizations,
        security=authorizations
    )

    api.add_namespace(register_api)
    api.add_namespace(login_api)
    api.add_namespace(image_api)
    app.register_blueprint(bp)

def register_extension(app):
    db.init_app(app)

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    
    jwt = JWTManager(app)

    register_extension(app)
    register_blueprint(app)
    app.register_blueprint(root)

    return app
