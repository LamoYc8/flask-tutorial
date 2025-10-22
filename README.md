# Flask Framework 学习代码实践

本项目用于学习与实践 **Flask Web 框架** 的核心功能与常用技术集成。通过此项目，可以了解从后端到前端的完整开发流程，包括路由管理、数据库交互、Redis 缓存、多线程处理与前端页面交互，为理解与实践 Serverless 架构奠定基础。

---

## 🧰 技术栈 (Tech Stack)

- **Python** - 后端开发语言  
- **Flask** - 轻量级 Web 框架  
- **MySQL** - 关系型数据库 
- **Redis** - 缓存，消息队列
- **Blueprint** - Flask 模块化应用结构  
- **Bootstrap** - 前端样式与布局框架  
- **jQuery** - 前端交互与 AJAX 支持  

---

## 🚀 Web项目结构 (Project Structure)

```
flask-blueprint-web/
├── app/
│   ├── __init__.py          # Flask 应用初始化 -> 蓝图注册,拦截器,js func注入
│   ├── views/               # View Functions -- route rules
│   │   ├── login.py
│   │   ├── order.py         
│   ├── templates/           # HTML 模板文件
│   └── static/              # 静态文件 (CSS / JS / images)
|   |__ utils/               # MySQL and Redis
├── requirements.txt         # 项目依赖包
└── app.py                   # 应用主入口

worker_fbw.py                # 后台具体业务执行
```

---

## ⚙️ 快速启动 (Quick Start)

1. **创建虚拟环境并安装依赖**
   ```bash
   pyenv global python@3.13
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **配置数据库**
   在 `/utils` 中修改你的 MySQL 连接信息：
   ```python
   POOL = PooledDB(
   creator=
   mincached=
   maxcached=
   .....

   host=
   port=
   passwd=
   db=
   )
   ```

3. **运行应用**
   ```bash
   flask run
   # 或者
   python app.py
   python worker_fbw.py
   ```

4. **访问页面**
   浏览器打开 [http://127.0.0.1:5050](http://127.0.0.1:5050)

---

## 💡 学习目标 (Learning Objectives)

- 掌握 Flask 的路由与蓝图机制  
- 实践数据库连接与 ORM 操作  
- 熟悉前后端交互（AJAX / jQuery）  
- 使用 Bootstrap 优化页面布局  

---

## 📄 License

This project is for educational purposes only.
