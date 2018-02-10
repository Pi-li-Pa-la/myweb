import pymysql.cursors
from config import db_config


db_config['cursorclass'] = pymysql.cursors.DictCursor


class Db(object):

    def __init__(self):
        self.session = pymysql.connect(**db_config)

    def all_table(self):
        result = []
        try:
            with self.session.cursor() as cursor:
                sql = '''
                    SELECT
                        table_name
                    FROM
                        information_schema.tables
                    WHERE
                        table_schema='{}' and table_type='base table';
                    '''.format(db_config['db'])
                cursor.execute(sql)
                for c in cursor:
                    result.append(c['table_name'])
                result.remove('alembic_version')

        finally:
            self.session.close()
            return result

    def all_columns(self, table_name):
        result = []
        try:
            with self.session.cursor() as cursor:
                sql = '''
                    SELECT
                        column_name
                    FROM
                        information_schema.columns
                    WHERE
                        table_schema ='{}'  and table_name = '{}';
                '''.format(db_config['db'], table_name)
                cursor.execute(sql)
                for c in cursor:
                    result.append(c['column_name'])

        finally:
            self.session.close()
            return result

if __name__ == '__main__':
    u = Db()
    l = u.all_columns('users')
    print(l)
