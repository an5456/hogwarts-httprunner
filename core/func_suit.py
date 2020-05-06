import logging
import random
import string

# 获取26个大小写字母
import time
from datetime import timedelta, date

import pymysql
import yaml, os

from core.data_curd import DataCurd

letters = string.ascii_letters
# 获取26个小写字母
Lowercase_letters = string.ascii_lowercase
# 获取26个大写字母
Capital = string.ascii_uppercase
# 获取阿拉伯数字
digits = string.digits

codelist = []


class FuncSuit:

    def test_2(self):
        ran = random.randint(0, 9)
        return str(ran)

    def test_1(self, info_data):
        print("hello world==={}".format(info_data["username"]))
        print("hello world==={}".format(info_data["password"]))
        return str(info_data["username"]) + "&" + info_data["password"]

    def telephone(self):
        """
            随机生成手机号
        :return:
        """
        # 第二位数字

        second = [3, 4, 5, 7, 8][random.randint(0, 4)]
        # 第三位数字
        third = {
            3: random.randint(0, 9),
            4: [5, 7, 9][random.randint(0, 2)],
            5: [i for i in range(10) if i != 4][random.randint(0, 8)],
            7: [i for i in range(10) if i not in [4, 9]][random.randint(0, 7)],
            8: random.randint(0, 9),
        }[second]
        # 最后八位数字
        suffix = random.randint(10000000, 99999999)

        # 拼接手机号
        telephone = "1{}{}{}".format(second, third, suffix)
        # logging.info("创建手机号：" + telephone)
        return telephone

    def create_telephone(self):
        telephone = random.choice(['177', '188', '185', '136', '158', '151']) + "".join(
            random.choice("0123456789") for i in range(8))
        print(telephone)
        return telephone

    def code(self):
        # s是小写字母和数字的集合
        s = Lowercase_letters + digits
        # 生成28位小写和数字的集合，并将列表转字符串
        code = ''.join(random.sample(s, 10))
        print('随机code:%s' % code)
        return code

    def r_string(self):  # 生成随机字符串
        data = "1234567890zxcvbnmlkjhgf#$%z%%%^dsaqwertyuiopABCDEFGHIGKLMNOP"
        # 用时间来做随机播种
        random.seed(time.time())
        # 随机选取数据
        sa = []
        for i in range(20):
            sa.append(random.choice(data))
        salt = "gp_" + ''.join(sa)
        print(salt)
        # return salt

    def get_token(self, lis=None):
        """读取yaml中信息"""
        if isinstance(lis, dict):
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "cookies.yaml")
            operation = open(path, "r", encoding="utf-8")
            return yaml.load(operation.read(), Loader=yaml.FullLoader).get("cookies")["cookie"]
        elif isinstance(lis, list):
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "cookies.yaml")
            operation = open(path, "r", encoding="utf-8")
            return yaml.load(operation.read(), Loader=yaml.FullLoader).get("cookies")["cookie"]
        else:
            path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "cookies.yaml")
            operation = open(path, "r", encoding="utf-8")
            return yaml.load(operation.read(), Loader=yaml.FullLoader).get("cookies")["cookie"]

    def select_data(self, data):
        self.connection = pymysql.connect(
            host='119.3.89.184',
            port=3308,
            user='root',
            password='test123456',
            db='test_db',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
        )
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(data["sql"])
                result = cursor.fetchone()
                return result.get(data["key"])
        finally:
            self.connection.close()


if __name__ == '__main__':
    # FuncSuit().telephone()
    # FuncSuit().create_telephone()
    # FuncSuit().code()
    # FuncSuit().r_string()
    # second = [3, 4, 5, 7, 8][random.randint(0, 4)]
    # print(second)
    a = {
        "sql": "select name from users where sex=19;",
        "key": "name"
    }
    print(FuncSuit().select_data(a))
