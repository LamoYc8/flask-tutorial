from flask import Blueprint, session, redirect

# Defining a blueprint for login function 
od = Blueprint('order', __name__, template_folder=None, static_folder=None)
# first parameter: the name give to the blueprint, will used for internal routing
# Blueprint package, locate the root_path for the blueprint


@od.route('/order/list')
def get_order_entity():
    # 统一由interceptor限制访问
    # 必须登录后查看    
    return '订单明细'


@od.route('/order', methods=['POST'])
def create_order():
    return 'order is placed!'
