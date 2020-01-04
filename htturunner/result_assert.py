import os, logging

from htturunner.runner import Runapi
from htturunner.utis import Utils


class Result:
    run = Runapi()

    @classmethod
    def result_assert(cls, path_1, filename):
        single_testcase_yaml = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tests", path_1, filename)
        result = cls.run.run_yml(single_testcase_yaml)

        if len(result) > 1:
            result1 = []
            if isinstance(result[0][0], list):
                for res in result:
                    for r in res:
                        result = r[0]
                        result1.append(result)
                result = result1
            else:
                for res in result:
                    result = res[0][0]
                    result1.append(result)
                result = result1
        elif len(result) > 1 and isinstance(result[0][0], list):
            result1 = []
            for res in result[0]:
                for r in res:
                    result = r[0]
                    result1.append(result)
            result = result1
        elif len(result[0]) > 1:
            result2 = []
            for res in result[0]:
                result = res[0]
                result2.append(result)
            result = result2
        else:
            result = result[0][0]

        for ass in result:
            if ass.get("csv_name"):
                logging.info(20 * "=" + ass["name"] + "--" + ass["csv_name"] + 20 * "=")
            else:
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
                if vale["expected"] == vale["actual"]:
                    logging.info("{} expected:{} actual:{} PASS".format(vale["key"], vale["expected"], vale["actual"]))
                else:
                    logging.info("{} expected:{} actual:{} FAIL".format(vale["key"], vale["expected"], vale["actual"]))
                    raise AssertionError
