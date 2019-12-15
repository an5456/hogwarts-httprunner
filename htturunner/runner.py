import csv
import io
import random
import re
from json import JSONDecodeError
import jsonpath
import urllib3
from requests import sessions
import os
from htturunner.loader import load_yml
from htturunner.parse import ParseContent
from htturunner.validate import is_api, is_testcase
import warnings
import sys

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

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'


# 对应接口返回的json响应内容，使用jsonpath 提取想要的字段
class Runapi:
    def __init__(self):
        self.action = ParseContent(all_veriables_mapping)

    def extract_json_field(self, resp, json_field):
        value = jsonpath.jsonpath(resp.json(), json_field)
        return value[0]

    # 字段替换
    # def replace_var(content, variables_mapping):
    #     try:
    #         vars_list = []
    #         for var_tuple in variable_regex_compile.findall(content):
    #             vars_list.append(
    #                 var_tuple[0] or var_tuple[1]
    #             )
    #     except TypeError:
    #         return []
    #     if not vars_list:
    #         return content
    #
    #     var_name = vars_list
    #     # 同一行字符串替换两个字段
    #     if 1 < len(var_name) <= 2:
    #         value = variables_mapping[var_name[0]]
    #         value1 = variables_mapping[var_name[1]]
    #         replace_content = content.replace("${%s}" % var_name[0], str(value)).replace("${%s}" % var_name[1], str(value1))
    #     # 同一行字符串，替换三个字段
    #     elif len(var_name) > 2:
    #         value = variables_mapping[var_name[0]]
    #         value1 = variables_mapping[var_name[1]]
    #         value2 = variables_mapping[var_name[2]]
    #         replace_content = content.replace("${%s}" % var_name[0], str(value)).replace("${%s}" % var_name[1],
    #                                                                                      str(value1)).replace(
    #             "${%s}" % var_name[2], str(value2))
    #     else:
    #         value = variables_mapping[var_name[0]]
    #         replace_content = content.replace("${%s}" % var_name[0], str(value))
    #     return replace_content

    # 解析请求是否含有类似${},如果有就替换
    # def parse_content(content, variables_mapping):
    #     if isinstance(content, dict):
    #         parsed_content = {}
    #         for key, value in content.items():
    #             parsed_value = parse_content(value, variables_mapping)
    #             parsed_content[key] = parsed_value
    #         return parsed_content
    #     elif isinstance(content, list):
    #         parsed_content = []
    #         for item in content:
    #             parsed_item = parse_content(item, variables_mapping)
    #             parsed_content.append(parsed_item)
    #         return parsed_content
    #     elif isinstance(content, str):
    #         matched = variable_regex_compile.findall(content)
    #         matched_function = function_regex_compile.findall(content)
    #
    #         if matched_function:
    #             return parse_funtion(content, all_veriables_mapping["config"]["variables"])
    #
    #         elif matched:
    #             return replace_var(content, variables_mapping)
    #         else:
    #             return content
    #
    #     else:
    #         return content

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
        self.get_run_api(api_info)
        request = api_info["request"]
        global session_variables_mapping
        # parsed_request = parse_content(request, session_variables_mapping)
        # method = parsed_request.pop("method")
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
            variables = all_veriables_mapping["config"]["variables"]

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
                    csv_info = self.load_csv()  # 解析csv参数
                    for csv_dict in csv_info:
                        parsed_config = self.action.parse_content(variables, csv_dict)  # 解析variables中是否需要替换的参数，如${}
                        parsed_request = self.action.parse_content(request, parsed_config)  # 解析request中是否需要替换参数，如${}
                        variables_request = self.action.parse_content(api_info["validate"],
                                                                      parsed_config)  # 解析断言部分validate是否有替换的参数,如：${}
                        try:
                            """判断是否有设置verify，绕过ssh验证"""
                            verify = all_veriables_mapping["config"]["verify"]
                            parsed_request["verify"] = verify
                        except KeyError:
                            pass
                        method = parsed_request.pop("method")
                        url = parsed_request.pop("url")
                        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                        reps = session.request(method, url, **parsed_request)
                        print(FAIL+"==============="+csv_dict["dec"]+ENDC)
                        print(HEADER+"url "+str(url)+ENDC)
                        print(HEADER+"method "+method+ENDC)
                        print(HEADER+"request_data "+str(parsed_request)+ENDC)
                        print()
                        # validator_mapping = variables_request["validate"]
                        # 响应断言如果断言的key里面有"$"就用jsonpath获取断言的结果
                        # 如果没有"$"就用一般的json规则去提取数据
                        for key in variables_request:
                            if "$" in key:
                                actual_value = str(self.extract_json_field(reps, key))
                            else:
                                actual_value = getattr(reps, key)  # 实际结果
                            expected_value = variables_request[key]  # 预期结果
                            try:
                                if isinstance(actual_value, int) or isinstance(expected_value, int):
                                    actual_value = int(actual_value)
                                    expected_value = int(expected_value)
                                    assert actual_value == expected_value
                                else:
                                    assert actual_value == expected_value
                                    print(WARNING + "pass" + ENDC)
                            except AssertionError:
                                print("\033[1;31m=======AssertionError=====\033[0m")
                                print("\033[1;36mexpected:\033[0m" + '\n\t' + "{}={}".format(key, expected_value))
                                print("\033[1;32mactual:\033[0m" + '\n\t' + "{}={}".format(key, actual_value))

                        try:
                            info = reps.json()
                            print(info)
                        except JSONDecodeError:
                            print(reps)
                        # 提取响应参数
                        extract_mapping = api_info.get("extract", {})
                        for var_name in extract_mapping.keys():
                            var_expr = extract_mapping[var_name]
                            var_value = self.extract_json_field(reps, var_expr)
                            session_variables_mapping[var_name] = var_value
                    return True
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
                    print(OKGREEN + 'urls=='+ENDC+'{}'.format(url))
                    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                    reps = session.request(method, url, **parsed_request)
                    print(OKGREEN+reps.url+ENDC)
                    try:
                        info = reps.json()
                        print(info)
                    except JSONDecodeError:
                        print(reps)
                    extract_mapping = api_info.get("extract", {})
                    for var_name in extract_mapping.keys():
                        var_expr = extract_mapping[var_name]
                        var_value = self.extract_json_field(reps, var_expr)
                        session_variables_mapping[var_name] = var_value
        else:
            parsed_request = self.action.parse_content(request, session_variables_mapping)
            method = parsed_request.pop("method")
            url = parsed_request.pop("url")
            print(url)
            print(WARNING + ' failed{}'.format(url) + ENDC)
            print("\033[1;32m{}:\033[0m".format(url))
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            reps = session.request(method, url, **parsed_request)
            print("444444" + reps.url)
            try:
                info = reps.json()
                print(info)
            except JSONDecodeError:
                pass
            # requests 每一次调用都会创建一个session，所以用同一个session访问
            # 响应断言如果断言的key里面有"$"就用jsonpath获取断言的结果
            # 如果没有"$"就用一般的json规则去提取数据
            validator_mapping = api_info["validate"]
            for key in validator_mapping:
                if "$" in key:
                    actual_value = self.extract_json_field(reps, key)
                else:
                    actual_value = getattr(reps, key)  # 实际结果
                expected_value = validator_mapping[key]  # 预期结果
                # assert actual_value == expected_value
                try:
                    if isinstance(actual_value, int) or isinstance(expected_value, int):
                        actual_value = int(actual_value)
                        expected_value = int(expected_value)
                        assert actual_value == expected_value
                    else:
                        assert actual_value == expected_value
                except AssertionError:
                    print("\033[1;31m=======AssertionError=====\033[0m")
                    print("\033[1;36mexpected:\033[0m" + '\n\t' + "{}={}".format(key, expected_value))
                    print("\033[1;32mactual:\033[0m" + '\n\t' + "{}={}".format(key, actual_value))
            try:
                info = reps.json()
                print(info)
            except JSONDecodeError:
                print(reps.text)
            # 提取响应参数
            extract_mapping = api_info.get("extract", {})
            for var_name in extract_mapping.keys():
                var_expr = extract_mapping[var_name]
                var_value = self.extract_json_field(reps, var_expr)
                session_variables_mapping[var_name] = var_value

            return True

    def run_yml(self, yml_file):
        """运行yml文件"""
        result = []
        load_content = load_yml(yml_file)
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

    def load_veritable(self, yml_file):
        load_content = load_yml(yml_file)
        return load_content

    # 获取依赖接口
    def get_run_api(self, api_info):
        file_path = os.path.dirname(os.path.dirname(__file__)) + "/tests/"
        if api_info.get("api"):
            ru_path = os.path.join(file_path, api_info.get("api"))
            print("依赖运行了")
            self.load_veritable(ru_path)
            self.run_yml(ru_path)

    def load_csv(self):
        csv_file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(csv_file_path + "/data/", "login.csv")
        csv_content_list = []

        with io.open(path, encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                csv_rander = csv.DictReader(csvfile, fieldnames=row)
                for row in csv_rander:
                    csv_dict = dict(row)
                    csv_content_list.append(csv_dict)
        return csv_content_list
        # if isinstance(args, list):
        #     for value in csv_content_list:
        #         for key in args:
        #             print(value[key])
        # else:
        #     print("{} not is list".format(args))

    # def test_1(username=None, password=None):
    #     print("hello world==={}".format(username))
    #     print("hello world==={}".format(password))
    #     return username + str(password)

    def test_2(self):
        ran = random.randint(0, 9)
        return ran
    # from htturunner.func_suit import FuncSuit
    #
    # # 获取模块中的类的方法名，并执行
    # def res(fun_name):
    #     f = FuncSuit.__dict__
    #     if fun_name in f:
    #        return f[fun_name](FuncSuit())

    # 解析函数，并替换
    # def parse_funtion(str_1, info_dict):
    #     """
    #     :param str_1: 需要解析的字符串 类似：https://mubu.com/${test_2()}
    #     :param info_dict: 需要替换的数据
    #     :return: 被替换后的字符串 ，类似：https://mubu.com/17729678
    #     """
    #     result_dict = {}
    #     parse_list = []
    #     regx_data = function_regex_compile.findall(str_1)
    #     try:
    #         if regx_data:
    #             for i in regx_data:
    #                 if "$" in i[1]:
    #                     for re_data in variable_regex_compile.findall(i[1]):
    #                         parse_list.append(re_data[0] or re_data[1])
    #                     for value in parse_list:
    #                         try:
    #                             result_dict[value] = info_dict[value]
    #                         except Exception as e:
    #                             print(e)
    #                     ret = str_1.replace("${%s($%s,$%s)}" % (regx_data[0][0], parse_list[0], parse_list[1]),
    #                                         test_1(**result_dict))
    #                     return ret
    #                 else:
    #                     return str_1.replace("${%s()}" % (regx_data[0][0]), str(res(regx_data[0][0])))
    #     except Exception as e:
    #         print("=====" + e)





if __name__ == '__main__':
    str_1 = "xxxs:${test_1($username,$password)}ssss:wwwww"
    test_dict = {"username": "zhangsan", "password": 123456, "age": 21}
    print(Runapi().action.parse_funtion(str_1, test_dict))

