import redis, json, hashlib

# 池化redis connection 
REDIS_POOL = redis.ConnectionPool(host='127.0.0.1', port=6379, encoding='utf-8', max_connections=50)
TASK_QUEUE = 'spider_task_list'
RESULT_QUEUE = 'spider_result_dict'


def get_task():
    
    conn = redis.Redis(connection_pool=REDIS_POOL)
    data = conn.brpop(TASK_QUEUE, timeout=10)
    if not data:
        return
    # block popping from the right of the list, wait for 10s, in case consume too much cpu

    # brpop will return a tuple: data=('spider_task_list', 'task_dict')
    # we only need the second value
    return json.loads(data[1].decode('utf-8'))

def set_result(tid: int, sign: str):
    
    conn = redis.Redis(connection_pool=REDIS_POOL) 
    conn.hset(RESULT_QUEUE, tid, sign)
    
def run():
    # infinite loop to catch the incoming task
    while True:
        # 1. obtain the task 
        task_dict = get_task()
        print(task_dict)
        if not task_dict:
            continue

        # 2. execute the time-consuming task
        ordered_string = task_dict['data']
        encrypt_string = ordered_string + "560c52ccd288fed045859ed18bffd973"
        obj = hashlib.md5(encrypt_string.encode('utf-8'))
        sign = obj.hexdigest() 

        # 3. push the result of task to the result_list
        tid = task_dict['id']
        set_result(tid, sign)

if __name__ == '__main__':
    run()