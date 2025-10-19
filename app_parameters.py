from flask import Flask, request, jsonify
app = Flask(__name__)


# http://host:port?age=1%pwd=123    ---> exec index GET default
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return index_post()
    
    else:
        age = request.args.get('age')
        pwd = request.args.get('pwd')
        print(age, pwd)
    
    return 'function index works'

# http://host:port/index    ---> POST + parameters in body
# v1=123&v2=321
# {"v1": "123", "v2": "321"}
def index_post():
    var1 = request.form.get('v1')
    var2 = request.form.get('v2')
    print(var1, var2)

    # body form is in JSON
    print(request.json, type(request.json))

    # return 'index post completed!'
    # jsonify will stream the dict type
    return jsonify({"status": True, "data": "Index post func completed"})

@app.route('/test')
def test():
    return 'running test function'


if __name__ == '__main__':
    app.run(port=5050)
    # 指明 host, port number