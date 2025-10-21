from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    # Generate a random key to encrypt the session inform

    from .views import login, order

    app.register_blueprint(login.usrLogin)
    app.register_blueprint(order.od)

    return app 