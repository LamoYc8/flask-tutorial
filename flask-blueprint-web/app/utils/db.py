import pymysql
from pymysql import cursors

from dbutils.pooled_db import PooledDB

POOL = PooledDB(
    creator=pymysql,
    maxconnections=10,
    mincached=2,
    maxcached=3,
    blocking=True, # conn demands more 10, then new request is blocking
    setsession=[], # when starting the connection, the cmd that we could execute
    ping=0, # build-in feature, check the current connection works or not

    # following parameters can be the db related inform
    # host, port, pwd, db_name......
    host='127.0.0.1', port=3306, user='root', passwd='1357901111', db='flask_web'
)

def fetch_one(sql, params) -> dict:
    conn = POOL.connection()
    cursor = conn.cursor(cursor=cursors.DictCursor)
    # Return value type will be dict 
    cursor.execute(sql, params)
    result = cursor.fetchone()
    cursor.close()
    conn.close() # 不是关闭conn, 交回给pool

    return result 

def fetch_all(sql, params) -> dict:
    conn = POOL.connection()
    cursor = conn.cursor(cursor=cursors.DictCursor)
    cursor.execute(sql, params)
    result = cursor.fetchall()
    cursor.close()
    conn.close() # 不是关闭conn, 交回给pool

    return result
    

def create_one(sql, params) -> int:
    conn = POOL.connection()
    cursor = conn.cursor(cursor=cursors.DictCursor)
    cursor.execute(sql, params)

    # create, update, delete operation need commit
    conn.commit()
    
    cursor.close()
    conn.close() # 不是关闭conn, 交回给pool

    # return the auto-increased id 
    return cursor.lastrowid