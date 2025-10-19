from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

@app.route('/sign', methods=['POST'])
def sign():
    """
    请求的数据格式: { "ordered_string": "..."}
    Keyword arguments:
    argument -- description
    Return: return_description
    """
    # obtain JSON from the client and parse 'ordered_string' from it
    ordered_string = request.json.get('ordered_string')
    if not ordered_string:
        return jsonify({'status': False, 'error': 'parameters not included!'})

    # create the signature 
    encrypt_string = ordered_string + "560c52ccd288fed045859ed18bffd973"
    obj = hashlib.md5(encrypt_string.encode('utf- 8'))

    sign = obj.hexdigest() 
    return jsonify({'status': True, 'data': sign})



if __name__ == '__main__':
    app.run(port=5050)