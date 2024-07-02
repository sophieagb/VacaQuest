import os
from flask import Flask
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv

load_dotenv()

bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__, template_folder="../frontend/templates", static_folder="../frontend/static")
    app.secret_key = os.urandom(24)
    
    app.config["MYSQL_HOST"] = os.getenv("MYSQL_HOST")
    app.config["MYSQL_USER"] = os.getenv("MYSQL_USER")
    app.config["MYSQL_PASSWORD"] = os.getenv("MYSQL_PASSWORD")
    app.config["MYSQL_DB"] = os.getenv("MYSQL_DB")

    bcrypt.init_app(app)
    
    from app.backend.routes import main_bp
    app.register_blueprint(main_bp)

    return app
