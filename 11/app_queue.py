from flask import Flask, request, jsonify
import hashlib, uuid, redis, json

app = Flask(__name__)

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

    # create the ID
    tid = str(uuid.uuid4())

    # 1. 放入队列中
    task_dict = {'id': tid, 'data': ordered_string}

    REDIS_CONN_PARAMS = {
        'host': '127.0.0.1',
        # 'password': 'qwe123',
        'port': 6379,
        'encoding': 'utf-8'
    }

    conn = redis.Redis(**REDIS_CONN_PARAMS)
    conn.lpush('spider_task_list', json.dumps(task_dict))
    """
    redis = {
    task_list1:[]
    task_list2:[]
    spider_task_list:[]
    }
    """

    # 2. return task ID to the caller
    return jsonify({'status': True, 'data': tid, 'message': 'The request is under processing, please come back later to check the result.'})




    """
    encrypt_string = ordered_string + "560c52ccd288fed045859ed18bffd973"
    obj = hashlib.md5(encrypt_string.encode('utf- 8'))

    sign = obj.hexdigest() 
    return jsonify({'status': True, 'data': sign})
    """

if __name__ == '__main__':
    app.run(port=5050, debug=True)



# Redis focused 