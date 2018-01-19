from flask import Blueprint, render_template, request, redirect, url_for
from models.User import User


main = Blueprint('user', __name__)


@main.route('/', methods=['GET'])
def index():
    return render_template('/user/login.html')


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    u = User(form)
    status, msg = u.valid()
    print('status:', status)
    print('msg:', msg)
    return redirect(url_for('.index'))
