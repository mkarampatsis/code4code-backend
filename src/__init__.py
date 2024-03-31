from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from mongoengine import connect
from src.config import JWT_SECRET_KEY, MONGO_DBNAME, MONGO_HOST, MONGO_PORT
from src.blueprints.auth import auth
from src.blueprints.ml import ml
from src.blueprints.exercises import exercises
from src.blueprints.evaluation import evalExercises

app = Flask(__name__)
jwt = JWTManager(app)
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY

CORS(
    app,
    resources={r"*": {"origins": ["http://localhost:4200", "https://code4code.ddns.net"]}},
)

connect(
    alias=MONGO_DBNAME,
    db=MONGO_DBNAME,
    host=MONGO_HOST,
    port=MONGO_PORT,
)

app.register_blueprint(auth, url_prefix="/auth")
app.register_blueprint(ml, url_prefix="/ml")
app.register_blueprint(exercises, url_prefix="/exercises" )
app.register_blueprint(evalExercises, url_prefix="/evaluation" )
