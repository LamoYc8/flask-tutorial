from flask import Blueprint, render_template, request, redirect, session
import pymysql

from ..utils import db

# Defining a blueprint for login function 
usrLogin = Blueprint('usrLogin', __name__, template_folder='..templates', static_folder='..static')
# first parameter: the name give to the blueprint, will used for internal routing
# Blueprint package, locate the root_path for the blueprint


@usrLogin.route('/login', methods=['POST', 'GET'])
def usr_login():
    if request.method == 'GET':
        # 执行登录页面渲染
        return render_template('login.html') # under templates folder 

    # Args from html form submission
    role = request.form.get('role')
    usr_name = request.form.get('usr_name')
    pwd = request.form.get('pwd')
    print(role, usr_name, pwd)

    # Verify the user inform with the stored data inside database
    # create connection to MySQL database --> pool connection
    sql = 'select * from usr_inform where role=%s and usr_name=%s and password=%s'
    user_dict = db.fetch_one(sql, [role, usr_name, pwd])
    print(user_dict)

    if user_dict:
        # Login succeed
        # Also create session id stored in cookie to maintain login status
        session['usr_inform'] = {'id': user_dict['id'], 'role': user_dict['role'], 'real_name': user_dict['real_name']}
        return redirect('/order/list')
    return render_template('login.html', error='User inform is incorrect!') 
    # sending error key back to the html pageU