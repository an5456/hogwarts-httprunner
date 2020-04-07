import logging

import pymysql
from core.getlog import GetLog


class DataCurd:
    GetLog().set_log_config_1()

    def __init__(self):
        self.connection = pymysql.connect(
            host='119.3.89.184',
            port=3308,
            user='root',
            password='test123456',
            db='test_db',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
        )
        logging.info("创建数据库连接")

    def insert_data(self, sql):
        try:
            with self.connection.cursor() as cursor:
                # sql = "insert into users (name, sex) values (\"dachui\", 34)"
                # # logging.info("执行的sql但是没有提交："+sql)
                # name = "王12"
                # sex = 22
                cursor.execute(sql)
                logging.info("执行的sql但是没有提交：" + sql)
                # raise NameError
                self.connection.commit()
                logging.info("sql已执行并提交到数据库")
        finally:
            self.connection.close()
            logging.info("数据库连接已关闭")

    def select_data(self, sql):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchone()
                return result
        finally:
            self.connection.close()


if __name__ == '__main__':
    a = "insert into users (name, sex) values ('777227007', 36);"
    b = "select name from users where sex=19;"
    # DataCurd().insert(a)
    print(DataCurd().select_data(b).get("name"))
