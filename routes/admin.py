import time
from flask import Blueprint, render_template, redirect, url_for, request
from models.Db import Db
from utils import log, valid_int_type
from functools import reduce
from universal_func import csrf, csrf_func, valid_csrf, current_user, login_required

main = Blueprint('admin', __name__)
db = Db()


# 此函数用来生成sql语句，拆分出来是为了代码的简洁易维护
def make_insert_sql(form, table_name):
    # 从form中删除csrf。由于flask返回的form不是dict，所以必须遍历一遍
    d = {}
    for k, v in form.items():
        if k != 'csrf':
            d[k] = v

    # 将键值分别组合为sql要求的格式并执行
    key = reduce(lambda x, y: x + ", " + y, d.keys())
    value = "'" + reduce(lambda x, y: x + "', '" + y, d.values()) + "'"
    sql = "INSERT INTO {}({}) VALUES ({});".format(table_name, key, value)
    return sql


def make_update_sql(form, id, table_name):
    # 从form中删除csrf。由于flask返回的form不是dict，所以必须遍历一遍
    d = {}
    for k, v in form.items():
        if k != 'csrf':
            d[k] = v

    # 将键值分别组合为sql要求的格式并执行
    l = []
    for k, v in d.items():
        l.append(k + " = '" + v + "'")
    sql = "UPDATE {} SET {} WHERE id={};".format(table_name, ','.join(l), id)
    print(sql)
    return sql


# 此函数获取数据库指定表的列信息，并将处理过的列信息返回
def column_info_func(table_name):
    col_info = db.column_info(table_name)
    for c in col_info:
        if c['COLUMN_KEY'] == 'PRI':
            col_info.remove(c)
        elif c['Extra'] == 'auto_increment':
            col_info.remove(c)
        elif c['COLUMN_NAME'] == 'time':
            col_info.remove(c)
    return col_info


# 此函数用来检测传入的数据格式是否符合要求
# 从路由函数中单独拆分出来是为了保证代码的简洁易于维护
# 因为需要考虑繁杂的可能性，因此目前只检查数据库中已出现的数据格式
def valid_data_type(form, col_info):
    for k, v in form.items():
        for name in col_info:
            # 当列名（COLUMN_NAME）相同时，name['DATA_TYPE']属性规定了v值的格式
            if k == name['COLUMN_NAME']:
                # 数据为int格式时的逻辑
                if name['DATA_TYPE'] == 'int':
                    if not valid_int_type(v):
                        return False, 'int类型数据格式错误'
                    else:
                        return True, ''
                # 数据为varchar格式时的逻辑
                elif name['DATA_TYPE'] == 'varchar':
                    if (k == 'username') and not ((len(v) > 6) and (len(v) < 32)):
                        return False, '用户名格式错误'
                    elif (k == 'password') and not ((len(v) > 7) and (len(v) < 129)):
                        return False, '密码格式错误'
                    # elif (k == 'salt') and (len(v) == 64):
                    elif k == 'salt' and not (len(v) > 5):
                        return False, '盐格式错误'
                    return True, ''
    return False, '未找到该列'


@main.route('/', methods=['GET'])
@login_required
def index():
    return render_template('/admin/admin.html')


@main.route('/db', methods=['GET'])
@login_required
def data_base():
    table_list = db.all_table()
    return render_template('/admin/db_list.html', table=table_list)


@main.route('/db/<string:table_name>', methods=['GET'])
@login_required
def table(table_name):
    column_name = db.all_columns(table_name)
    data = db.column_data(table_name)
    username=current_user()
    csrf_token = csrf_func(username)
    return render_template('/admin/table.html', tableName=table_name, columnName=column_name, tableData=data, csrfToken=csrf_token)


@main.route('/db/insert/<string:table_name>', methods=['GET', 'POST'])
@login_required
def insert_data(table_name):
    # col_info 存放处理过的数据表列信息。
    col_info = column_info_func(table_name)
    username = current_user().username

    # 当请求此页面时
    if request.method.upper() == 'GET':
        csrf_token = csrf_func(username)
        return render_template('/admin/db_add.html', tableName=table_name, columns=col_info, csrfToken=csrf_token)

    # 当请求插入数据时
    elif request.method.upper() == 'POST':
        form = request.form
        if not valid_csrf(form['csrf'], username):
            log('我曹，跨站请求伪造？', request.form)
            return render_template('/admin/db_add.html', tableName=table_name, columns=col_info, csrfToken=csrf_func(username), msg='跨站请求伪造！！！')

        valid_result, msg = valid_data_type(form, col_info)
        if not valid_result:
            return render_template('/admin/db_add.html', tableName=table_name, columns=col_info, csrfToken=csrf_func(username), msg=msg)

        sql = make_insert_sql(form, table_name)
        db.diu_sql(sql)
        print(sql)
        return redirect(url_for('.table', table_name=table_name))


@main.route('/db/update/<string:table_name>', methods=['GET', 'POST'])
@login_required
def update_data(table_name):
    # col_info 存放处理过的数据表列信息。
    col_info = column_info_func(table_name)
    username = current_user().username
    query = request.args
    id = query['id']
    row = db.select_by_id(table_name, id)

    # 当请求此页面时
    if request.method.upper() == 'GET':
        csrf_token = csrf_func(username)
        return render_template('/admin/db_update.html', tableName=table_name, columns=col_info, row=row[0],
                               csrfToken=csrf_token)

    # 当请求插入数据时
    elif request.method.upper() == 'POST':
        form = request.form
        if not valid_csrf(form['csrf'], username):
            log('我曹，跨站请求伪造？', request.form)
            return render_template('/admin/db_update.html', tableName=table_name, columns=col_info, row=row[0],
                                   csrfToken=csrf_func(username), msg='跨站请求伪造！！！')

        valid_result, msg = valid_data_type(form, col_info)
        if not valid_result:
            return render_template('/admin/db_update.html', tableName=table_name, columns=col_info, row=row[0],
                                   csrfToken=csrf_func(username), msg=msg)

        sql = make_update_sql(form, id, table_name)
        db.diu_sql(sql)
        return redirect(url_for('.table', table_name=table_name))


@main.route('/db/delete/<string:table_name>', methods=['GET'])
@login_required
def delete_data(table_name):
    args = request.args
    username = current_user().username
    csrf_token = args['csrfToken']
    if valid_csrf(csrf_token, username):
        id = args['id']
        sql = "DELETE FROM {} WHERE id={}".format(table_name, id)
        db.diu_sql(sql)
    return redirect(url_for('.table', table_name=table_name))