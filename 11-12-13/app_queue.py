from flask import Flask, request, jsonify
import hashlib, uuid, redis, json

app = Flask(__name__)

# 池化redis connection 
REDIS_POOL = redis.ConnectionPool(host='127.0.0.1', port=6379, encoding='utf-8', max_connections=50)
TASK_QUEUE = 'spider_task_list'
RESULT_QUEUE = 'spider_result_dict'

@app.route('/task', methods=['POST'])
def task():
    """
    receive the caller request
    create a task ID and return it back to the caller
    queue the task

    request data format in body: { "ordered_string": "..."}
    Return: return_description
    """
    # obtain JSON from the request body and parse 'ordered_string' from it
    # if request does not include json, the server will complain unsupported media type
    ordered_string = request.json.get('ordered_string')
    if not ordered_string:
        return jsonify({'status': False, 'error': 'parameters not included!'})

    # create the task ID
    tid = str(uuid.uuid4())

    # 1. 放入队列中
    task_dict = {'id': tid, 'data': ordered_string}

    conn = redis.Redis(connection_pool=REDIS_POOL)
    conn.lpush(TASK_QUEUE, json.dumps(task_dict))
    """
    redis = {
    task_list1:[]
    task_list2:[]
    spider_task_list:[]
    }
    """

    # 2. return task ID to the caller
    return jsonify({'status': True, 'task_id': tid, 'message': 'The request is under processing, please come back later to check the result.'})

# section 13 
@app.route('/result')
def result():
    # url: host:port/result?tid=xxx

    id = request.args.get('tid')
    if not id:
        return jsonify({'status': False, 'error': 'parameters not included!'})


    conn = redis.Redis(connection_pool=REDIS_POOL)
    sign = conn.hget(RESULT_QUEUE, id)
    if not sign:
        return jsonify({'status': True, 'data':'', 'message': 'Still in processing, please wait for a while!'})
    
    sign_str = sign.decode('utf-8')
    conn.hdel(RESULT_QUEUE, id) # fetch and then delete it from the result queue


    return jsonify({'status': True, 'data': sign_str})



if __name__ == '__main__':
    app.run(port=5050, debug=True)



# Redis focused 