import redis, json, hashlib

def get_task():
    REDIS_CONN_PARAMS = {
        'host': '127.0.0.1',
        # 'password': 'qwe123',
        'port': 6379,
        'encoding': 'utf-8'
    }
    conn = redis.Redis(**REDIS_CONN_PARAMS)
    data = conn.brpop('spider_task_list', timeout=10)
    if not data:
        return
    # block popping from the right of the list, wait for 10s, in case consume too much cpu

    # brpop will return a tuple: data=('spider_task_list', 'task_dict')
    # we only need the second value
    return json.loads(data[1].decode('utf-8'))

def set_result(tid: int, sign: str):
    REDIS_CONN_PARAMS = {
        'host': '127.0.0.1',
        # 'password': 'qwe123',
        'port': 6379,
        'encoding': 'utf-8'
    }
    conn = redis.Redis(**REDIS_CONN_PARAMS) 
    conn.hset('spider_result_dict', tid, sign)
    
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