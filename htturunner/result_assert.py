import os, logging

from htturunner.runner import Runapi
from htturunner.utis import Utils


class Result:
    run = Runapi()
    @classmethod
    def result_assert(cls, path_1, filename):
        single_testcase_yaml = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tests", path_1, filename)
        result = cls.run.run_yml(single_testcase_yaml)
        for ass in result[0]:
            logging.info(20 * "=" + ass["name"] + 20 * "=")
            logging.info("url:" + ass["url"])
            logging.info("method:" + ass["method"])
            if ass["request_info"].get("type") == "json":
                logging.info("request_data:" + "\n" + Utils.format_output(ass["request_data"]))
                logging.info("response_data:" + "\n" + Utils.format_output(ass["response_data"]))
            else:
                logging.info("request_data:" + str(ass["request_data"]))
                logging.info("response_data:" + str(ass["response_data"]))
            logging.info(10 * "-" + "Assert" + 10 * "-")
            for vale in ass["assert_data"]:
                logging.info("{} expected:{} actual:{}".format(vale["key"], vale["expected"], vale["actual"]))
                assert vale["expected"] == vale["actual"]

