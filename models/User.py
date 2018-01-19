import hashlib
# import os
from . import ModelMixin
from . import db


class User(db.Model, ModelMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, form):
        self.username = form.get('username')
        self.password = form.get('password')

    def valid(self):
        pass


    # def valid_username(self):
    #     print(self.query.filter_by(username=self.username))
    #     return len(self.query.filter_by(username=self.username).all()) == 0
    #
    # def valid(self):
    #     valid_username = self.valid_username()
    #     valid_username_len = len(self.username) >= 6
    #     valid_password_len = len(self.password) >= 6
    #     msgs = []
    #     if not valid_username:
    #         message = '用户名已存在'
    #         msgs.append(message)
    #     if not valid_username_len:
    #         message = '用户名长度必须大于等于6'
    #         msgs.append(message)
    #     if not valid_password_len:
    #         message = '密码长度必须大于等于6'
    #         msgs.append(message)
    #     status = (not valid_username) and valid_username_len and valid_password_len
    #     return status
