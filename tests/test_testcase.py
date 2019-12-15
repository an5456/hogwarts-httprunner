import os

import allure

from htturunner.runner import Runapi


def setup_module():
    print("模块之前")


def teardown_module():
    print("模块之后")


@allure.feature("测试接口")
class TestSingle:

    def setup(self):
        print("每个测试用例之前运行")

    def teardown(self):
        print("每个测试用例之后执行")

    def setup_class(self):
        print("每个类之前运行")

    def teardown_class(self):
        print("每个类之后运行")

    # def test_loader_single_testcase(self):
    #     """加载出的用例内容和原始信息一致
    #     """
    #     single_testcase_yaml = os.path.join(os.path.dirname(__file__), "testcase", "mubu_login.yml")
    #     loaded_json = load_yml(single_testcase_yaml)
    # self.assertIsInstance(loaded_json, list)
    # self.assertEqual(len(loaded_json), 2)
    run = Runapi()

    @allure.story("测试1")
    def test_run_testcase_yml(self):
        """

            斤斤计较测试
        """
        single_testcase_yaml = os.path.join(os.path.dirname(__file__), "testcase", "mubu_login.yml")
        result = self.run.run_yml(single_testcase_yaml)
        print(result)

    @allure.story("测试2")
    def test_run_login(self):
        """

            范德萨范德萨
        """
        single_testcase_yaml = os.path.join(os.path.dirname(__file__), "api", "get_login.yml")
        result = self.run.run_yml(single_testcase_yaml)

    @allure.story("测试3")
    def test_get_login_submit(self):
        """ 呵呵呵呵1234"""
        single_testcase_yaml = os.path.join(os.path.dirname(__file__), "api", "get_login_submit.yml")

        result = self.run.run_yml(single_testcase_yaml)
        assert result[0] == True

    @allure.story("测试4")
    def test_get_home_page(self):
        """

            测试呵呵呵呵
        """
        single_testcase_yaml = os.path.join(os.path.dirname(__file__), "api", "get_home_page.yml")
        result = self.run.run_yml(single_testcase_yaml)
        allure.attach.file("/Users/anxiaodong/PycharmProjects/hogwarts-httprun/data/login.csv", "报告", allure.attachment_type.CSV)
        print(result)
