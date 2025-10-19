import redis, json

REDIS_CONN_PARAMS = {

        'host': '127.0.0.1',
        # 'password': 'qwe123', no pwd for the current config
        'port': 6379,
        'encoding': 'utf-8'
    }

conn = redis.Redis(**REDIS_CONN_PARAMS)
conn.lpush('test_task_list', json.dumps({'id': 1, 'data': 'hello'}))

conn.lpush('test_task_list', json.dumps({'id': 2, 'data': 'world'}))

data = conn.rpop('test_task_list')
print(data)