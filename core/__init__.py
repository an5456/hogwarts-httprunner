# from requests.compat import basestring
#
# a="fdafdsaf"
# b = isinstance(a, basestring)
# print(b)

# import os
# ile_path = os.path.dirname(os.path.dirname(__file__))
# print(ile_path)

# docker run -d --name mariadb -e ALLOW_EMPTY_PASSWORD=yes -e MARIADB_USER=bn_testlink -e MARIADB_DATABASE=bitnami_testlink  -p 8088:3306 bitnami/mariadb:latest
#
# docker run -p 3306:3306 --name mysqldb -v /root/docker-mysql/conf:/etc/mysql -v /root/docker-mysql/logs:/var/log -v /root/docker-mysql/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=test123456 -d mysql:5.7
#
# docker run --name mysqldb -v /root/docker-mysql/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=test123456 -p 8888:3306  -d mysql:5.7
#
#
# docker run --name mydb -p 3306:3306 -v /root/docker-mysql/data:/var/lib/mysql -v /root/docker-mysql/conf:/etc/mysql -v /root/docker-mysql/logs:/var/log -e MYSQL_ROOT_PASSWORD=test123456 -d mysql:5.7
#
# docker run --name prometheus -d -p 9090:9090 -v /root/prometheus.yml:/etc/prometheus/prometheus.yml  prom/prometheus --config.file=/root/prometheus.yml
#
# docker run -d --name mysql-exporter -p 9104:9104 -e DATA_SOURCE_NAME="root:test123456.@(119.3.89.184:3306)/mysql" prom/mysqld-exporter
# from os import _wrap_close
# import os
#
#
# # 源码
#
#
#
# def popen(cmd, mode="r", buffering=-1):
#     if not isinstance(cmd, str):
#         raise TypeError("invalid cmd type (%s, expected string)" % type(cmd))
#     if mode not in ("r", "w"):
#         raise ValueError("invalid mode %r" % mode)
#     if buffering == 0 or buffering is None:
#         raise ValueError("popen() does not support unbuffered streams")
#     import subprocess, io
#     if mode == "r":
#         proc = subprocess.Popen(cmd,
#                                 shell=True,
#                                 stdout=subprocess.PIPE,
#                                 bufsize=buffering)
#         return _wrap_close(io.TextIOWrapper(proc.stdout), proc)
#     else:
#         proc = subprocess.Popen(cmd,
#                                 shell=True,
#                                 stdin=subprocess.PIPE,
#                                 bufsize=buffering)
#         return _wrap_close(io.TextIOWrapper(proc.stdin), proc)

#
# adb = "pytest -v /Users/anxiaodong/PycharmProjects/hogwarts-httprun/tests/test_testcase.py"
# d = os.popen(adb)
# print(d.read())
import os

# print(os.path.dirname(os.path.dirname(__file__)))
# print(os.path.dirname(os.path.dirname(__file__)))
# print(os.path.join(os.path.dirname(os.path.dirname(__file__)), "test"))