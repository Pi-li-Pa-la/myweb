import pymysql.cursors
from config import db_config


db_config['cursorclass'] = pymysql.cursors.DictCursor


class Db(object):

    def __init__(self):
        self.session = ''

    def select_sql(self, sql):
        result = []
        self.session = pymysql.connect(**db_config)
        try:
            with self.session.cursor() as cursor:
                cursor.execute(sql)
                for c in cursor:
                    result.append(c)
        finally:
            self.session.close()
            return result

    def diu_sql(self, sql):
        self.session = pymysql.connect(**db_config)
        # 下边的注释是用来告诉pycharm宽泛的错误提示也可以。这样可以阻止too broad exception clause提示。
        # noinspection PyBroadException
        try:
            with self.session.cursor() as cursor:
                cursor.execute(sql)
                self.session.commit()
        except:
            self.session.rollback()
        finally:
            self.session.close()

    def all_table(self):
        result = []
        sql = '''
            SELECT
                table_name
            FROM
                information_schema.tables
            WHERE
                table_schema='{}' and table_type='base table';
            '''.format(db_config['db'])
        data = self.select_sql(sql)
        for d in data:
            result.append(d['table_name'])
        result.remove('alembic_version')
        return result

    def all_columns(self, table_name):
        result = []
        sql = '''
            SELECT
                column_name
            FROM
                information_schema.columns
            WHERE
                table_schema ='{}'  and table_name = '{}';
            '''.format(db_config['db'], table_name)
        data = self.select_sql(sql)
        for d in data:
            result.append(d['column_name'])
        return result

    def column_data(self, table_name):
        result = []
        sql = '''
            SELECT
                *
            FROM
                {}
            ORDER BY
                id;
            '''.format(table_name)
        data = self.select_sql(sql)
        for d in data:
            result.append(d)
        return result

    def column_info(self, table_name):
        sql = '''
            SELECT 
                COLUMN_NAME,COLUMN_KEY,COLUMN_DEFAULT,IS_NULLABLE,Extra,DATA_TYPE
            FROM 
                INFORMATION_SCHEMA.COLUMNS 
            WHERE 
                table_name='{}' 
            AND 
                table_schema='{}';
            '''.format(table_name, db_config['db'])
        result = self.select_sql(sql)
        return result

    def select_by_id(self, table_name, *args):
        # 此函数根据id查询
        l = []
        for arg in args:
            l.append(str(arg))
        where = ' OR id='.join(l)

        sql = """
            SELECT
                *
            FROM
                {}
            WHERE
                id={}
        """.format(table_name, where)
        result = self.select_sql(sql)
        return result


if __name__ == '__main__':
    u = Db()
    # sql = """
    #         SELECT
    #             *
    #         FROM
    #             users
    #         WHERE
    #             2
    #     """
    # l = u.select_by_id('users', "1 or 2 or 3")
    # # l = u.column_info('users')
    l = u.select_by_id('users', 1, 2, 3)
    print(l)
    # print(',,,'.join(['1', '2', '3']))

    # print(int(-11))
