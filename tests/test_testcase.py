import os
import allure
from core.result_assert import Result


def setup_module():
    print("模块之前")


def teardown_module():
    print("模块之后")


@allure.feature("测试接口")
class TestSingle:

    @allure.story("测试1")
    def test_run_testcase_yml(self):
        """斤斤计较测试"""
        Result.result_assert("testcase", "mubu_login.yml")

    @allure.story("测试2")
    def test_run_login(self):
        """范德萨范德"""
        Result.result_assert("api/json", "get_login.json")

    @allure.story("测试登陆123")
    def test_get_login_submit(self):
        """ 呵呵呵呵1234"""
        Result.result_assert("api/yml", "get_login_submit.yml")

    @allure.story("测试4")
    def test_get_home_page(self):
        """测试呵呵呵呵"""
        Result.result_assert("api/yml", "get_home_page.yml")
        allure.attach.file(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "login.csv"), "报告",
                           allure.attachment_type.CSV)

    @allure.story("上传文件")
    def test_upfile(self):
        Result.result_assert("api/yml", " .yml")

    @allure.story("创建客户")
    def test_addcustomer(self):
        Result.result_assert("api/yml", "addcustomer.yml")
