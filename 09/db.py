from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import os

# ---------- Flask & SQLite 配置 ----------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------- 定义数据库模型 ----------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    token = db.Column(db.String(120), unique=True, nullable=False)

# ---------- 初始化数据库 ----------
if not os.path.exists('data.db'):
    with app.app_context():
        db.create_all()

# ---------- 搭建管理界面 ----------
admin = Admin(app, name='Demo Admin', template_mode='bootstrap3')
admin.add_view(ModelView(User, db.session))

# ---------- REST API ----------
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'name': u.name, 'token': u.token} for u in users])

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({'id': user.id, 'name': user.name, 'token': user.token})

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'name' not in data or 'token' not in data:
        return jsonify({'error': 'name and token required'}), 400
    user = User(name=data['name'], token=data['token'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'user created', 'id': user.id}), 201

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    if 'name' in data:
        user.name = data['name']
    if 'token' in data:
        user.token = data['token']
    db.session.commit()
    return jsonify({'message': 'user updated'})

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'user deleted'})

# ---------- 启动服务 ----------
if __name__ == '__main__':
    app.run(port=3306, debug=True)


# 启动服务： python db.py
# 打开网页后台： http://127.0.0.1:3306/admin
# 调用REST API （Postman or curl）
# db model modified, need to delete instance db and rerun the db.py to recreate the db
