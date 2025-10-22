import redis, json


REDIS_POOL = redis.ConnectionPool(host='127.0.0.1', port=6379, encoding='utf-8', max_connections=50)
TASK_QUEUE = 'task_todo_list'
RESULT_QUEUE = 'spider_result_dict'


def append(task: dict):
    conn = redis.Redis(connection_pool=REDIS_POOL)
    conn.lpush(TASK_QUEUE, json.dumps(task))