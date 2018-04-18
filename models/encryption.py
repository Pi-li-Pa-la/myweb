import sys

from . import db
from . import ModelMixin


class EncryptAccount(db.Model, ModelMixin):
    __tablename__ = "encrypt_account"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32))
    aes_password = db.Column(db.String(128))
    web_site = db.Column(db.String(128))
    remark = db.Column(db.Text())
    create_time = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user = db.relationship("User", backref=db.backref('users', lazy=True))

    def __init__(self, form):
        self.username = form.get("username", "")
        self.aes_password = form.get("aes_password", "")
