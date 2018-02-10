from flask import Blueprint, render_template, redirect, url_for
from models.Db import Db


main = Blueprint('admin', __name__)


@main.route('/', methods=['GET'])
def index():
    return render_template('/admin/admin.html')


@main.route('/db', methods=['GET'])
def db():
    db = Db()
    table_list = db.all_table()
    return render_template('/admin/db_list.html', table=table_list)


@main.route('/db/<string:table_name>', methods=['GET'])
def table(table_name):
    db = Db()
    column_name = db.all_columns(table_name)
    return render_template('/admin/table.html', tableName=table_name, columnName=column_name)