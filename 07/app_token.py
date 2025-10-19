from flask import Flask, request, jsonify
import hashlib

app = Flask(__name__)

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

    
    # verify the incoming token 
    usr_dict = get_usr_inform()
    if token not in usr_dict:
        
        return jsonify({'status': False, 'error': 'Token is not valid!'})

    # obtain JSON from the client and parse 'ordered_string' from it
    ordered_string = request.json.get('ordered_string')
    if not ordered_string:
        return jsonify({'status': False, 'error': 'parameters not included!'})

    # create the signature 
    encrypt_string = ordered_string + "560c52ccd288fed045859ed18bffd973"
    obj = hashlib.md5(encrypt_string.encode('utf- 8'))

    sign = obj.hexdigest() 
    return jsonify({'status': True, 'data': sign})

def get_usr_inform():
    inform_dict = dict()
    with open('token.txt', mode='r', encoding='utf-8') as f:
        for line in f:
            token, name = line.strip().split(',')
            inform_dict[token] = name
    
    return inform_dict
            

if __name__ == '__main__':
    app.run(port=5050)