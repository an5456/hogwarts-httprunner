
import subprocess

if __name__ == '__main__':
    subprocess.run("pytest -s --alluredir=./report;"
                   "allure generate ./report -o ./html --clean;"
                   , shell=True)
