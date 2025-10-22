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
    #print(usr_inform)
    if role == 1:
        # select * from order where usr_id=%s
        id = usr_inform['id']
        order_list = db.fetch_all("select * from `order` left join usr_inform on `order`.usr_id = usr_inform.id where usr_id=%s", [id]) # order 和程序内重名有冲突
    else:
        # select * from order 
        order_list= db.fetch_all("select * from `order` left join usr_inform on `order`.usr_id = usr_inform.id", [])
    
    print(order_list)
    # 优化表格显示，赋予meaning, instead of numeric items
    # based on the status presents different color theme
    status = {
        1: {'text':'Waiting', 'cls': 'primary'},
        2: {'text':'In process', 'cls': 'info'},
        3: {'text':'Completed', 'cls': 'success'},
        4: {'text':'Failed', 'cls': 'danger'},
    }

    real_name = usr_inform['real_name']
    # display the query result 
    return render_template('order_list.html', list=order_list, status_dict=status)


@od.route('/order/create', methods=['GET'])
def create_order():
    return render_template('order_create.html')
