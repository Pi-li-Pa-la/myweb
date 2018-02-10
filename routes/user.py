from flask import Blueprint, render_template, request, redirect, url_for, abort
from models.User import User, RegisterCode
from utils import log


main = Blueprint('user', __name__)


@main.route('/', methods=['GET'])
def index():
    return render_template('/user/login.html')


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    u = User(form)
    # status, msg = u.valid()
    # print('status:', status)
    # print('msg:', msg)
    return redirect(url_for('.index'))


@main.route('/register', methods=['GET'])
def register():
    return render_template('/user/register.html')


@main.route('/signup', methods=['POST'])
def signup():
    form = request.form
    u = form.get('username', '')
    pwd = form.get('password', '')
    pwd_ag = form.get('password_again', '')
    r_code = form.get('register_code', '')

    u_len = False
    u_status = False
    p_len = False
    p_status = False
    r_code_status = False

    if (len(u) > 5) and (len(u) < 33):
        u_len = True
    if not User.query.filter_by(username=u).all():
        u_status = True
    if (len(pwd) > 8) and (len(pwd) < 128):
        p_len = True
    if pwd == pwd_ag:
        p_status = True
    if RegisterCode.query.filter_by(value=r_code).all():
        r_code_status = True
    return redirect(url_for('.index'))


@main.route('/confirm_username', methods=['GET', 'POST'])
def confirm_u():
    form = request.form
    u = form.get('username', '')
    if (u != '') and (not User.query.filter_by(username=u).all()):
        return 'OK'
    return 'OK', 202
