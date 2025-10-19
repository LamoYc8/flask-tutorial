from flask import Flask, request, jsonify
import hashlib
from dbutils.pooled_db import PooledDB
import pymysql

app = Flask(__name__)

# prepare the mysql db connection pool
POOL = PooledDB(
    creator=pymysql,
    maxconnections=10,
    mincached=2,
    maxcached=3,
    blocking=True,
    setsession=[], # when starting the connection, the cmd that we could execute
    ping=0, # build-in feature, check the current connection works or not

    # following parameters can be the db related inform
    # host, port, pwd, db_name......
)
# how to use 
conn = POOL.connection()
# ......
conn.close() # Not to close the connection, just to hand over it back to the pool


@app.route('/sign', methods=['POST'])
def sign():
    """
    request URL must have token attached: /sign?token=
    request data format in body: { "ordered_string": "..."}
    Return: return_description
    """
    # check if token is attached
    token = request.args.get('token')
    if not token:
        return jsonify({'status': False, 'error': 'Token is not attached!'})

    
    # verify the incoming token from the backend database
    usr_token = get_usr_inform()
    if token not in usr_token:
        
        return jsonify({'status': False, 'error': 'Token is not valid!'})

    # obtain JSON from the request body and parse 'ordered_string' from it
    # if request does not include json, the server will complain unsupported media type
    ordered_string = request.json.get('ordered_string')
    if not ordered_string:
        return jsonify({'status': False, 'error': 'parameters not included!'})

    # create the signature 
    encrypt_string = ordered_string + "560c52ccd288fed045859ed18bffd973"
    obj = hashlib.md5(encrypt_string.encode('utf- 8'))

    sign = obj.hexdigest() 
    return jsonify({'status': True, 'data': sign})

def get_usr_inform():
    import requests
    res = requests.get(
        url='http://127.0.0.1:3306/api/users'
    )

    users = res.json() # obtain Python dict
    usr_token = dict()
    for u in users:
        usr_token[u['token']] = u['name']
    
    return usr_token

if __name__ == '__main__':
    app.run(port=5050, debug=True)



# 为了轻量化，dev环境没有用真实MySQL，但是 connection pool 借用了 MySQL
# 学习知识就好