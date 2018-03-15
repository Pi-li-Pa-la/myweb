import time, binascii, os
from flask import session, redirect, url_for, request
from functools import wraps

from models.User import User
from utils import log


# 防止跨站伪造
csrf = []


# 维护csrf列表并生成新csrf
def csrf_func(username):
    # 删除超过10分钟的请求凭证,保证安全且没有垃圾信息
    for c in csrf:
        # 超过10分钟的csrf_token会被删除
        if time.time() - c['time'] > 600:
            log('time.time: ', time.time())
            log('-: ', time.time() - c['time'])
            csrf.remove(c)
        # 删除此用户名下的所有csrf_token
        elif c['username'] == username:
            csrf.remove(c)

    # 防止跨站请求伪造
    csrf_token = binascii.hexlify(os.urandom(32)).decode()
    csrf.append(dict(username=current_user().username,
                     csrf_token=csrf_token, time=time.time()))
    return csrf_token


# 验证csrf_token
def valid_csrf(csrf_token, username):
    for c in csrf:
        if csrf_token == c['csrf_token'] and username == c['username']:
            return True
    return False


# 根据cookie和session验证当前用户
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
            return redirect(url_for('user.index', next=request.url))
        else:
            return f(*args, **kwargs)
    return func
