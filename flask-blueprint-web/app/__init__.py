from flask import Flask, request, session, redirect
import os

def auth():
    print("Interceptor")

    # Don't intercept js files
    if request.path.startswith('/static'):
        return 
    
    if request.path == '/login':
        # anyone could use this page, just move on
        return 
    
    usr_inform = session.get('usr_inform')
    if usr_inform:
        return 
    
    return redirect('/login')




def create_app():
    app = Flask(__name__)
    app.secret_key = os.urandom(24)
    # Generate a random key to encrypt the session inform

    from .views import login, order

    app.register_blueprint(login.usrLogin)
    app.register_blueprint(order.od)
    
    # Interceptor feature starts here
    app.before_request(auth)
    return app 