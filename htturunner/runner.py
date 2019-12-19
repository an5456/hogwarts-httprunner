import csv
import io
import random
import re
from json import JSONDecodeError
import jsonpath
import urllib3
from requests import sessions
import os

from htturunner.loader import Load
from htturunner.parse import ParseContent
from htturunner.validate import is_api, is_testcase
import warnings
import sys
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

session = sessions.Session()
# # 匹配规则，例如：${test} 匹配后为：test
# variable_regex_compile = re.compile(r"\$\{(\w+)\}|\$(\w+)")
# # 匹配规则，例如：${func(${var_1}, ${var_2})}
# function_regex_compile = re.compile(r"\$\{(\w+)\(([\$\w\.\-/\s=,]*)\)\}")
# 提取的断言元素
session_variables_mapping = {}
# 获取的config设置内容
all_veriables_mapping = {}
# 返回需要的数据
result = []
res_dict = {}


# 对应接口返回的json响应内容，使用jsonpath 提取想要的字段
class Runapi:
    def __init__(self):
        self.action = ParseContent(all_veriables_mapping)

    def extract_json_field(self, resp, json_field):
        value = jsonpath.jsonpath(resp.json(), json_field)
        return value[0]

    def run_api(self, api_info):
        """

        :param api:
            {
                "request": {},
                "validate": {}
            }
        :return:

        """
        warnings.simplefilter("ignore", ResourceWarning)
        self.get_run_api(api_info)  # 判断是否获取依赖接口
        request = api_info["request"]
        global session_variables_mapping
        global result
        global result_dict

        # 有config时执行以下代码
        if all_veriables_mapping["config"]:
            try:
                base_url = all_veriables_mapping["config"]["base_url"]  #
                if len(base_url) < len(request["url"]):
                    request["url"] = request["url"]
                else:
                    request["url"] = base_url + "/" + request["url"]
            except KeyError:
                request["url"] = request["url"]

            # if all_veriables_mapping["config"].get("variables"):
            #     variables = all_veriables_mapping["config"].get("variables")
            # else:
            #     variables = None
            variables = all_veriables_mapping["config"].get("variables", None)

            if variables is not None:
                # csv_request = api_info
                for key, value in variables.items():
                    session_variables_mapping[key] = value
                """
                    config中的变量通过外部传入，类似：
                    variables:
                        username: ${username}
                        password: ${password}
                    执行以下代码
                """
                if "$" in str(variables):
                    csv_info = Load.load_csv()  # 解析csv参数
                    for csv_dict in csv_info:
                        parsed_config = self.action.parse_content(variables, csv_dict)  # 解析variables中是否需要替换的参数，如${}
                        parsed_request = self.action.parse_content(request, parsed_config)  # 解析request中是否需要替换参数，如${}
                        variables_request = self.action.parse_content(api_info["validate"],
                                                                      parsed_config)  # 解析断言部分validate是否有替换的参数,如：${}
                        try:
                            """判断是否有设置verify，绕过ssl验证"""
                            verify = all_veriables_mapping["config"]["verify"]
                            parsed_request["verify"] = verify
                        except KeyError:
                            pass
                        method = parsed_request.pop("method")
                        url = parsed_request.pop("url")
                        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                        reps = session.request(method, url, **parsed_request)

                        # validator_mapping = variables_request["validate"]
                        # 响应断言如果断言的key里面有"$"就用jsonpath获取断言的结果
                        # 如果没有"$"就用一般的json规则去提取数据
                        exp = []
                        for var_value in variables_request:
                            for key, value in var_value.items():
                                if "eq" in key:
                                    key = value[0]
                                    if "$" in key:
                                        actual_value = str(self.extract_json_field(reps, key))
                                    else:
                                        actual_value = getattr(reps, key)  # 实际结果
                                    expected_value = value[1]  # 预期结果

                                    if isinstance(actual_value, int) or isinstance(expected_value, int):
                                        actual_value = int(actual_value)
                                        expected_value = int(expected_value)
                                    reps_dict = {
                                        "expected": expected_value,
                                        "actual": actual_value,
                                        "key": key
                                    }
                                    exp.append(reps_dict)
                                logger.info(exp)
                        if parsed_request.get("data") is None:
                            parsed_request["data"] = None
                        try:
                            reps = reps.json()
                        except JSONDecodeError:
                            reps = reps.text
                        res_dict = {
                            "url": url,
                            "method": method,
                            "request_data": parsed_request["data"],
                            "response_data": reps,
                            "data": exp,
                            "request_info": api_info
                        }
                        result.append(res_dict)
                        # 提取响应参数
                        self.extract_data(api_info, reps)
                    return result
                else:
                    """
                        confing中的variables变量的key直接输入的，执行以下方法，类似：
                        variables:
                            username: 17729597958
                            password: 123456
                    """
                    parsed_request = self.action.parse_content(request, session_variables_mapping)
                    try:
                        verify = all_veriables_mapping["config"]["verify"]
                        parsed_request["verify"] = verify
                    except KeyError:
                        pass
                    method = parsed_request.pop("method")
                    url = parsed_request.pop("url")
                    print(url)
                    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                    reps = session.request(method, url, **parsed_request)
                    self.extract_data(api_info, reps)  # 提取响应信息
        else:
            parsed_request = self.action.parse_content(request, session_variables_mapping)
            method = parsed_request.pop("method")
            url = parsed_request.pop("url")
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            reps = session.request(method, url, **parsed_request)
            # requests 每一次调用都会创建一个session，所以用同一个session访问
            # 响应断言如果断言的key里面有"$"就用jsonpath获取断言的结果
            # 如果没有"$"就用一般的json规则去提取数据
            validator_mapping = api_info["validate"]
            exp = []
            for var_value in validator_mapping:
                for key, value in var_value.items():
                    if "eq" in key:
                        key = value[0]
                        if "$" in key:
                            actual_value = str(self.extract_json_field(reps, key))
                        else:
                            actual_value = getattr(reps, key)  # 实际结果
                        expected_value = value[1]  # 预期结果

                        if isinstance(actual_value, int) or isinstance(expected_value, int):
                            actual_value = int(actual_value)
                            expected_value = int(expected_value)
                        reps_dict = {
                            "expected": expected_value,
                            "actual": actual_value,
                            "key": key
                        }
                        exp.append(reps_dict)
                    logger.info(exp)
            if parsed_request.get("data") == None:
                parsed_request["data"] = None
            try:
                reps = reps.json()
            except JSONDecodeError:
                reps = reps.text
            res_dict = {
                "url": url,
                "method": method,
                "request_data": parsed_request["data"],
                "response_data": reps,
                "data": exp,
                "request_info": api_info
            }
            result.append(res_dict)
            # 提取响应参数
            self.extract_data(api_info, reps)
        return result
        # for key in validator_mapping:
        #     if "$" in key:
        #         actual_value = self.extract_json_field(reps, key)
        #     else:
        #         actual_value = getattr(reps, key)  # 实际结果
        #     expected_value = validator_mapping[key]  # 预期结果
        #     # assert actual_value == expected_value
        #     try:
        #         if isinstance(actual_value, int) or isinstance(expected_value, int):
        #             actual_value = int(actual_value)
        #             expected_value = int(expected_value)
        #             assert actual_value == expected_value
        #         else:
        #             assert actual_value == expected_value
        #     except AssertionError:
        #         pass
        # # 提取响应参数
        # self.extract_data(api_info, reps)
        #
        # return True

    def run_yml(self, yml_file):
        """运行yml文件"""
        result = []
        load_content = Load.load_yml(yml_file)
        global all_veriables_mapping
        all_veriables_mapping["config"] = load_content.get("config", {})

        if is_api(load_content.get("teststeps")):
            success = self.run_api(load_content.get("teststeps"))
            result.append(success)
        elif is_testcase(load_content.get("teststeps")):
            for api_info in load_content.get("teststeps"):
                success = self.run_api(api_info)
                result.append(success)
        else:
            raise Exception("YAML format invalid".format(yml_file))

        return result

    # 获取依赖接口
    def get_run_api(self, api_info):
        file_path = os.path.dirname(os.path.dirname(__file__)) + "/tests/"
        if api_info.get("api"):
            ru_path = os.path.join(file_path, api_info.get("api"))
            print("依赖运行了")
            Load.load_yml(ru_path)
            self.run_yml(ru_path)

    def extract_data(self, api_info, reps):
        """提取响应断言信息"""
        extract_mapping = api_info.get("extract", {})
        for var_name in extract_mapping.keys():
            var_expr = extract_mapping[var_name]
            var_value = self.extract_json_field(reps, var_expr)
            session_variables_mapping[var_name] = var_value


if __name__ == '__main__':
    str_1 = "xxxs:${test_1($username,$password)}ssss:wwwww"
    test_dict = {"username": "zhangsan", "password": 123456, "age": 21}
    print(Runapi().action.parse_funtion(str_1, test_dict))
