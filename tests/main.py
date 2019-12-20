import pytest
import subprocess

if __name__ == '__main__':
    # 获取系统类型，Mac还是Linux
    os_type = subprocess.run("``uname", shell=True)
    subprocess.run("pytest -s --alluredir=./report;"
                   "allure generate ./report -o ./html --clean;"
                   , shell=True)
    if os_type == "Darwin":
        pid = subprocess.run("ps -ef|grep http.server | grep -E '[0-9] python3'|awk '{print $2}'", shell=True)
    else:
        pid = subprocess.run("ps -ef|grep python3 |awk '{print $2}' |awk 'NR==1'", shell=True)
    # pid = subprocess.run("ps -ef|grep python3|grep 8899|awk '{print $2}' |awk 'NR==2'", shell=True)
    if pid is not "":
        subprocess.run("kill -9" + str(pid) + "", shell=True)
        print("kill report server ")
    print("start report server")
    subprocess.run("cd ./html;nohup python3 -m http.server 8899 ", shell=True)
