import os

import allure

from htturunner.getlog import GetLog
from htturunner.runner import Runapi

import logging




from htturunner.utis import Utils


def setup_module():
    print("模块之前")


def teardown_module():
    print("模块之后")


@allure.feature("测试接口")
class TestSingle:

    def setup(self):
        logging.info("每个测试用例之前运行")

    def teardown(self):
        print("每个测试用例之后执行")

    def setup_class(self):
        print("每个类之前运行")

    def teardown_class(self):
        print("每个类之后运行")

    GetLog().set_log_config_1()
    run = Runapi()

    @allure.story("测试1")
    def test_run_testcase_yml(self):
        """

            斤斤计较测试
        """
        single_testcase_yaml = os.path.join(os.path.dirname(__file__), "testcase", "mubu_login.yml")
        result = self.run.run_yml(single_testcase_yaml)


    @allure.story("测试2")
    def test_run_login(self):
        """

            范德萨范德萨
        """
        single_testcase_yaml = os.path.join(os.path.dirname(__file__), "api", "get_login.yml")
        result = self.run.run_yml(single_testcase_yaml)
        logging.info("hhhhhhhhhhhhh")

    @allure.story("测试登陆123")
    def test_get_login_submit(self):
        """ 呵呵呵呵1234"""
        single_testcase_yaml = os.path.join(os.path.dirname(__file__), "api", "get_login_submit.yml")
        result = self.run.run_yml(single_testcase_yaml)
        # for ass in result[0]:
        #     logging.info("url:" + ass["url"])
        #     logging.info("method:" + ass["method"])
        #     if ass["request_info"].get("type") == "json":
        #
        #         logging.info("request_data:"+"\n"+Utils.format_output(ass["request_data"]))
        #         logging.info("response_data:"+"\n"+Utils.format_output(ass["response_data"]))
        #
        #     else:
        #         logging.info("request_data:"+str(ass["request_data"]))
        #         logging.info("response_data:"+str(ass["response_data"]))
        #     logging.info("----------------" + "Assert" + "------------------")
        #     for vale in ass["data"]:
        #         logging.info("{} expected:{} actual:{}".format(vale["key"], vale["expected"], vale["actual"]))
        #         assert vale["expected"] == vale["actual"]
        print(result)

    @allure.story("测试4")
    def test_get_home_page(self):
        """

            测试呵呵呵呵
        """
        single_testcase_yaml = os.path.join(os.path.dirname(__file__), "api", "get_home_page.yml")
        result = self.run.run_yml(single_testcase_yaml)
        for ass in result[0]:
            logging.info("url:" + ass["url"])
            logging.info("method:" + ass["method"])
            if isinstance(ass["request_info"], dict):
                    if ass["request_info"].get("type") == "json":

                        logging.info("request_data:"+Utils.format_output(ass["request_data"]))
                        logging.info("response_data:" +Utils.format_output(ass["response_data"]))

                    else:
                        logging.info("request_data:" + str(ass["request_data"]))
                        logging.info("response_data:" + str(ass["response_data"]))
            logging.info("----------------" + "Assert" + "------------------")
            for vale in ass["data"]:
                logging.info("{} expected:{} actual:{}".format(vale["key"], vale["expected"], vale["actual"]))
                assert vale["expected"] == vale["actual"]
        print(result)

        allure.attach.file(os.path.join(os.path.dirname(os.path.dirname(__file__)+"data"+"login.csv")), "报告",allure.attachment_type.CSV)

