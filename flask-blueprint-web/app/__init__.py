from flask import Flask, request, session, redirect
import os

def _auth():
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

# fetch client real name based on the session inform 
# provide the func for html file utilization
def _fetch_client_name():
    client_inform = session.get('usr_inform')
    return client_inform['real_name']


def create_app():
    app = Flask(__name__)
    # Generate a random key to encrypt the session inform
    # app.secret_key = os.urandom(24)
    app.secret_key = 'my_super_secret_key_123456' # 开发用这个，否则每次重启key都会改变session 

    from .views import login, order

    app.register_blueprint(login.usrLogin)
    app.register_blueprint(order.od)
    
    # Interceptor feature starts here
    app.before_request(_auth)

    # func inject to be globalized to the every html file 
    app.template_global()(_fetch_client_name)


    return app 