from flask import Flask
from app.routes import svnManager
import logging

def create_app():
    app = Flask(__name__)

    app.register_blueprint(svnManager.bp)

    return app