from flask import Blueprint, session, redirect, render_template
from ..utils import db

# Defining a blueprint for login function 
od = Blueprint('order', __name__, template_folder=None, static_folder=None)
# first parameter: the name give to the blueprint, will used for internal routing
# Blueprint package, locate the root_path for the blueprint

# /order 路由规则下，统一由interceptor限制访问
# 必须登录后查看    
@od.route('/order/list')
def get_order_list():
    usr_inform = session.get('usr_inform')

    role = usr_inform['role'] # 1: client; 2: admin
    print(usr_inform)
    if role == 1:
        # select * from order where usr_id=%s
        id = usr_inform['id']
        order_list = db.fetch_all("select * from `order` where usr_id=%s", [id]) # order 和程序内重名有冲突
    else:
        # select * from order 
        order_list= db.fetch_all('select * from `order`', [])
    
    # display the query result 
    return render_template('order_list.html', list=order_list)


@od.route('/order', methods=['POST'])
def create_order():
    return 'order is placed!'
