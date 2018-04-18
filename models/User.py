import hashlib, re, binascii, os
from . import ModelMixin
from . import db


class User(db.Model, ModelMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    password = db.Column(db.String(64))
    salt = db.Column(db.String(64))
    public_key = db.Column(db.String(1024))

    def __init__(self, form):
        self.username = form.get('username', '')
        self.password = form.get('password', '')
        self.salt = form.get('salt', self.make_salt())
        self.public_key = form.get("public_key", "")

    def valid_username(self):
        u = self.username
        if len(u) < 6 or len(u) > 32:
            return '用户名长度应在6到32位之间', 202
        if not re.match("^[A-Za-z0-9_]*$", u):
            # 这个正则表达式的意思是判断u是否由规定字符串构成
            return '用户名只能由字母、数字及下划线组成', 202
        return '用户名可以使用', 200

    def valid_password(self):
        p = self.password
        if len(p) < 8 or len(p) > 128:
            return '密码长度应在8到128位之间', 202
        # 利用正则表达式达到验证账户名和密码是否包含非法字符
        # https://codeday.me/bug/20170721/43023.html
        if not re.match("^[-A-Za-z0-9_+=~!@#$%^&;:?<>\[\]{}(),./*]*$", p):
            return "密码只能由数字、字母及_-/+=~!@#$%^&;:?<>,.[]{}()组成", 202
        return '密码可以使用', 200

    def encrypt(self, pwd):
        hax1 = hashlib.sha256(pwd.encode('ascii'))
        salt = self.salt + hax1.hexdigest()
        hax2 = hashlib.sha256(salt.encode('ascii'))
        return hax2.hexdigest()

    def valid_login(self):
        u = User.query.filter_by(username=self.username.lower()).first()
        if u:
            hax1 = hashlib.sha256(self.password.encode('ascii'))
            salt = u.salt + hax1.hexdigest()
            hax2 = hashlib.sha256(salt.encode('ascii'))
            if u.password == hax2.hexdigest():
                return True
        return False

    @staticmethod
    def make_salt():
        salt = binascii.hexlify(os.urandom(32)).decode()
        return salt

    def save(self):
        self.password = self.encrypt(self.password)
        db.session.add(self)
        db.session.commit()


class RegisterCode(db.Model):
    __tablename__ = 'register_code'
    id = db.Column(db.Integer, primary_key=True)
    value= db.Column(db.String(128))
    remarks = db.Column(db.String(128))

    def __init__(self, form):
        self.value = form['value']
        self.remarks = form['remarks']
