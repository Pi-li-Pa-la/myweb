from flask import Blueprint, render_template, request, redirect, url_for, abort, make_response, session
from models.User import User, RegisterCode
from functools import wraps
from utils import log
import re

main = Blueprint('user', __name__)


def current_user():
    # 通过cookie验证用户登录状态
    uid = session.get('user_id')
    if uid is not None:
        u = User.query.get(int(uid))
        return u
    return None


def login_required(f):
    @wraps(f)
    def func(*args, **kwargs):
        if current_user() is None:
            # 用户未登录，重定向到登录页面
            return redirect(url_for('.index', next=request.url))
        else:
            return f(*args, **kwargs)
    return func


@main.route("/", methods=["GET"])
def index():
    msg = ''
    next_url = request.args.get('next', '')
    if request.referrer == request.url:
        msg="帐号或密码错误，请重新输入"
    elif (not current_user()) & (next_url != ''):
        msg="进行此操作前请先登录"
    url = url_for('.login', next=next_url)
    if not next_url:
        # 如果next_url为空，我们让链接干净些
        url = url_for('.login')
    return render_template('/user/login.html', msg=msg, url=url)


@main.route('/<int:id>', methods=["GET"])
@login_required
def profile(id):
    u = current_user()
    if u.id != id:
        return abort(404)
    return render_template('/user/profile.html', user=u)


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    u = User(form)
    if u.valid_login():
        u = User.query.filter_by(username=u.username).first()
        session['user_id'] = u.id
        # args中的next属性如果被设置说明是由其他网页跳转过来的，若没设置则跳转到用户页面
        next_url = request.args.get('next', str(url_for('.profile', id=u.id)))
        return redirect(next_url)
    return redirect(url_for('.index'))


@main.route('/register', methods=['GET'])
def register():
    return render_template('/user/register.html')


@main.route('/signup', methods=['POST'])
def signup():
    form = request.form
    u = User(form)
    pwd = form.get('password', 'pwd')
    pwd_ag = form.get('password_again', 'pwd_ag')
    r_code = form.get('register_code', '')

    msg = u.valid_username()
    if msg[1] == 202:
        return render_template('/user/register.html', message=msg[0])

    msg = u.valid_password()
    if msg[1] == 202:
        return render_template('/user/register.html', message=msg[0])
    if pwd != pwd_ag:
        return render_template('/user/register.html', message='两次输入的密码不一致')

    u.save()
    return render_template('/user/register.html', message='注册成功')


@main.route('/confirm_username', methods=['GET', 'POST'])
def confirm_u():
    form = request.form
    u = User(form)
    return u.valid_username()


@main.route('/confirm_password', methods=['GET', 'POST'])
def confirm_pwd():
    form = request.form
    u = User(form)
    return u.valid_password()
