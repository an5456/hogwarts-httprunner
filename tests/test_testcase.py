import os
from htturunner.runner import run_yml


def setup_module():
    print("模块之前")


def teardown_module():
    print("模块之后")


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

    def test_run_testcase_yml(self):
        single_testcase_yaml = os.path.join(os.path.dirname(__file__), "testcase", "mubu_login.yml")
        result = run_yml(single_testcase_yaml)
        print(result)

    def test_run_login(self):
        single_testcase_yaml = os.path.join(os.path.dirname(__file__), "api", "get_login.yml")
        result = run_yml(single_testcase_yaml)

    def test_get_login_submit(self):
        single_testcase_yaml = os.path.join(os.path.dirname(__file__), "api", "get_login_submit.yml")
        result = run_yml(single_testcase_yaml)
    def test_get_home_page(self):
        single_testcase_yaml = os.path.join(os.path.dirname(__file__), "api", "get_home_page.yml")
        result = run_yml(single_testcase_yaml)
