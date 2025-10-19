from flask import Flask

app = Flask(__name__)

# /xxx -> execute the attached function
# url bounded with the function 
# In general, func-name align with url 
@app.route('/')
def index():
    return 'Hello World'


@app.route('/test')
def test():
    return 'running test function'


if __name__ == '__main__':
    app.run(host='localhost', port=5050)
    # 指明 host, port number