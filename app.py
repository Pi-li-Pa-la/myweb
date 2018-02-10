from flask import Flask, render_template
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from models import db
from routes.user import main as user_routes
from routes.admin import main as admin_routes
# import model


app = Flask(__name__)
manager = Manager(app)


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


def configured_app():
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    import config
    app.secret_key = config.secret_key
    app.config['SQLALCHEMY_DATABASE_URI'] = config.db_uri
    # 初始化db
    db.init_app(app)
    # 注册路由
    register_routes(app)
    # 配置日志
    configure_log(app)
    return app


def configure_log(app):
    # 设置log，否则输出会被gunicorn吃掉
    # 但是如果app是debug模式则不用
    if not app.debug:
        import logging
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)


def configure_manager():
    # 这个函数用来配置命令行选项
    Migrate(app, db)
    manager.add_command('db', MigrateCommand)


def register_routes(app):
    # 在这个函数里import并注册蓝图
    app.register_blueprint(user_routes, url_prefix='/user')
    app.register_blueprint(admin_routes, url_prefix='/admin')


# 自定义的命令行命令用来运行服务器
@manager.command
def server():
    app = configured_app()
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=3000,
    )
    app.run(**config)

if __name__ == '__main__':
    configure_manager()
    configured_app()
    manager.run()
elif __name__== 'app':
    configured_app()
