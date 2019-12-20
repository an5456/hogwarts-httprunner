import os

import allure

from htturunner.runner import Runapi

# import logging
#
# logger = logging.getLogger()
# logger.setLevel(logging.INFO)
from loguru import logger

from htturunner.utis import Utils


def setup_module():
    print("模块之前")


def teardown_module():
    print("模块之后")


@allure.feature("测试接口")
class TestSingle:

    def setup(self):
        logger.info("每个测试用例之前运行")

    def teardown(self):
        print("每个测试用例之后执行")

    def setup_class(self):
        print("每个类之前运行")

    def teardown_class(self):
        print("每个类之后运行")

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
        logger.info("hhhhhhhhhhhhh")

    @allure.story("测试登陆123")
    def test_get_login_submit(self):
        """ 呵呵呵呵1234"""
        single_testcase_yaml = os.path.join(os.path.dirname(__file__), "api", "get_login_submit.yml")
        print("jjjjjjjjjjjjjjjjjjjj")
        result = self.run.run_yml(single_testcase_yaml)
        #logger.info("666666666" + str(result))
        for ass in result[0]:
            logger.info("url:" + ass["url"])
            logger.info("method:" + ass["method"])
            if ass["request_info"].get("type") == "jsondumps":

                logger.info("request_data:"+"\n"+Utils.format_output(ass["request_data"]))
                logger.info("response_data:"+"\n"+Utils.format_output(ass["response_data"]))

            else:
                logger.info("request_data:"+str(ass["request_data"]))
                logger.info("response_data:"+str(ass["response_data"]))
            logger.info("----------------" + "Assert" + "------------------")
            for vale in ass["data"]:
                logger.info("{} expected:{} actual:{}".format(vale["key"], vale["expected"], vale["actual"]))
                assert vale["expected"] == vale["actual"]

    @allure.story("测试4")
    def test_get_home_page(self):
        """

            测试呵呵呵呵
        """
        single_testcase_yaml = os.path.join(os.path.dirname(__file__), "api", "get_home_page.yml")
        result = self.run.run_yml(single_testcase_yaml)
        #logger.info("666666666" + str(result))
        for ass in result[0]:
            logger.info("url:" + ass["url"])
            logger.info("method:" + ass["method"])
            if isinstance(ass["request_info"], dict):
                    if ass["request_info"].get("type") == "jsondumps":

                        logger.info(Utils.format_output(ass["request_data"]))
                        logger.info(Utils.format_output(ass["response_data"]))

                    else:
                        logger.info("request_data:" + str(ass["request_data"]))
                        logger.info("response_data:" + str(ass["response_data"]))
            else:
                logger.info("request_data:" + str(ass["request_data"]))
                logger.info("response_data:" + str(ass["response_data"]))
            logger.info("----------------" + "Assert" + "------------------")
            for vale in ass["data"]:
                logger.info("{} expected:{} actual:{}".format(vale["key"], vale["expected"], vale["actual"]))
                assert vale["expected"] == vale["actual"]
        #allure.attach.file("/Users/anxiaodong/PycharmProjects/hogwarts-httprun/data/login.csv", "报告",
                           #allure.attachment_type.CSV)

       # allure.attach.file("/Users/anxiaodong/PycharmProjects/hogwarts-httprun/data/login.csv", "报告", allure.attachment_type.CSV)
        print(result)
