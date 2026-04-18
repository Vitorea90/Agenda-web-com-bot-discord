from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)

    from app.controllers.agenda_controller import agenda_bp
    app.register_blueprint(agenda_bp)

    return app
