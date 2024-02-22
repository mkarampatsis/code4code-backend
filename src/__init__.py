from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from mongoengine import connect
from src.config import JWT_SECRET_KEY, MONGODB_URI
from src.blueprints.auth import auth
from src.blueprints.ml import ml

app = Flask(__name__)
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

CORS(app, resources={r"/*": {"origins": "*"}})

connect(host=MONGODB_URI, alias="code4code")

app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(ml, url_prefix="/ml")
