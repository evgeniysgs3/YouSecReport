import os
import sys
from flask import Flask
from flask_login import LoginManager
import bcrypt
from flask_pymongo import PyMongo
#from .database import db

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])
    #db.init_app(app)

    login_manager.init_app(app)

    import app.personalarea.views as personalarea

    app.register_blueprint(personalarea.personalarea)

    return app