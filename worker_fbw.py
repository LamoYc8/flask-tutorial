import redis, json, hashlib
from dbutils.pooled_db import PooledDB
from pymysql import cursors
import pymysql
from concurrent.futures import ThreadPoolExecutor

# 池化redis connection 
REDIS_POOL = redis.ConnectionPool(host='127.0.0.1', port=6379, encoding='utf-8', max_connections=50)
TASK_QUEUE = 'task_todo_list'
RESULT_QUEUE = 'task_result_dict'

# mysql connection pool
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

def _queue_init():
    # Only for dev env, push all prepared tasks to redis 
    # Don't use for pro env 

    # 1. fetch all tasks in 'waiting' status
    db_result = _fetch_all('select id from `order` where status=1', [])
        # ((1,), (2,), (4,), (7,), (8,), (9,), (10,), (11,))
    db_id_set = set([item[0] for item in db_result])
   
    # 2. fetch all tasks in the redis task_todo_list queue
    conn = redis.Redis(connection_pool=REDIS_POOL)
    queue_result = conn.lrange(TASK_QUEUE, 0, conn.llen(TASK_QUEUE))
    queue_set = set([int(item.decode('utf-8')) for item in queue_result])
    # data amount is not too big to block the redis memory

    # 3. only push those tasks which are not inside the queue
    data = db_id_set - queue_set
    if data:
        conn.lpush(TASK_QUEUE, *data) # push to queue with one time operation 

def _fetch_all(sql, params) -> tuple:
    conn = POOL.connection()
    # cursor = conn.cursor(cursor=cursors.DictCursor) 
    # default cursor will be tuple type, (id,) -> colon is required for any single element
    cursor = conn.cursor()
    cursor.execute(sql, params)
    result = cursor.fetchall()
    cursor.close()
    conn.close() # 不是关闭conn, 交回给pool

    return result

def _fetch_one(sql, params) -> tuple:
    conn = POOL.connection()
    cursor = conn.cursor(cursors.DictCursor)
    cursor.execute(sql, params)
    result = cursor.fetchone()
    cursor.close()
    conn.close() # 不是关闭conn, 交回给pool

    return result 

def _update_one(sql, params):
    conn = POOL.connection()
    cursor = conn.cursor(cursor=cursors.DictCursor)
    cursor.execute(sql, params)

    # create, update, delete operation need commit
    conn.commit()
    
    cursor.close()
    conn.close() # 不是关闭conn, 交回给pool

    


def _check_order(id: int):
    sql = 'select * from `order` where id=%s'
    result = _fetch_one(sql, [id])
    
    return result
    
def _update_order_status(id: int, status: int):
    sql = 'update `order` set status=%s where id=%s'
    _update_one(sql, [status, id])
    

def pop_queue():
    
    conn = redis.Redis(connection_pool=REDIS_POOL)
    data = conn.brpop(TASK_QUEUE, timeout=10)
    if not data:
        return
    # block popping from the right of the list, wait for 10s, in case consume too much cpu

    # brpop will return a tuple: data=(TASK_QUEUE, 'task_id')
    # we only need the second value
    return data[1].decode('utf-8')

def execute_task():
    pass
    # 具体的业务逻辑
    
def run():
    # 初始化数据库未在队列中的订单
    # 方便测试环境
    _queue_init()
    
    # infinite loop to catch the incoming task
    while True:
        # 1. obtain the task from the queue
        task_id = pop_queue()
        if not task_id:
            continue

        # 2. 检查订单是否依旧存在[用户可以进行删除操作]
        order = _check_order(task_id)
        if not order:
            continue
        
        # 3. update the order status: 'waiting' -> 'in process'
        _update_order_status(task_id, 2)
        
        # 4. execute the time-consuming task + multi-thread 
        print('订单执行中： ' + task_id)
        # create thread pool
        thread_pool = ThreadPoolExecutor(30)
        for i in range(order['count']):
            thread_pool.submit(execute_task, order) # 放入具体的业务逻辑&订单的相关信息
        
        thread_pool.shutdown()
        
        # 5. 执行完成，更新订单状态
        _update_order_status(task_id, 3)

if __name__ == '__main__':
    run()