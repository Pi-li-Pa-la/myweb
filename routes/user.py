from flask import Blueprint, render_template, request, redirect, url_for, abort
from models.User import User
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
    return redirect(url_for('.index'))


@main.route('/confirm_username', methods=['GET','POST'])
def confirm_u():
    form = request.form
    u = form.get('username', '')
    if User.query.filter_by(username=u).all() == 0:
        return 'OK'
    return 'ok', 202
