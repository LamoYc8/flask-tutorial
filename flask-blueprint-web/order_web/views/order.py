from flask import Blueprint, session, redirect

# Defining a blueprint for login function 
od = Blueprint('order', __name__, template_folder=None, static_folder=None)
# first parameter: the name give to the blueprint, will used for internal routing
# Blueprint package, locate the root_path for the blueprint


@od.route('/order/list')
def get_order_entity():
    # 1. 读取cookie and decrypt session inform
    usr_inform = session.get('usr_inform')
    #print(usr_inform, type(usr_inform))

    # No session no login inform, 
    # only allowed to view this page once the user has logged in 
    if not usr_inform:
        return redirect('/login')
    return '订单明细'


@od.route('/order', methods=['POST'])
def create_order():
    return 'order is placed!'
