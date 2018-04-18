# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, redirect, url_for, abort, session
from models.User import User, RegisterCode
from universal_func import current_user, login_required
from utils import log

main = Blueprint('user', __name__)


@main.route("/", methods=["GET"])
def index():
    if current_user():
        u_id = current_user().id
        return redirect(url_for('.profile', id=u_id))
    msg = ''
    next_url = request.args.get('next', '')
    # 这个条件判断的意思是，如果是由自己跳转来的
    if (request.referrer is not None) and (request.referrer.split('?')[0] == request.url):
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
    log('referrer: ', request.referrer)
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


@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method.upper() == "GET":
        return render_template('/user/register.html')

    elif request.method.upper() == "POST":
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
        u = User.query.filter_by(username=u.username).first()
        session['user_id'] = u.id
        return redirect(url_for('.profile', id=u.id))


@main.route('/confirm_username', methods=['GET', 'POST'])
def confirm_u():
    # 确认需注册的帐号是否合法，是否被占用
    form = request.form
    u = User(form)
    if u.query.filter_by(username=u.username.lower()).all():
        return '用户名已被占用', 202
    return u.valid_username()


@main.route('/confirm_password', methods=['GET', 'POST'])
def confirm_pwd():
    form = request.form
    u = User(form)
    return u.valid_password()


@main.route('/valid_username', methods=['GET', 'POST'])
def valid_username():
    form = request.form
    u = User(form)
    if u.username == 'admin':
        return '', 200
    log('valid_username: ', form, u.valid_username())
    return u.valid_username()
