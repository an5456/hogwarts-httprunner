from json import JSONDecodeError
import urllib3
from requests import sessions
import os

from htturunner.loader import Load
from htturunner.parse import ParseContent
from htturunner.utis import Utils
from htturunner.validate import is_api, is_testcase
import warnings
import sys
import logging

session = sessions.Session()
# # 匹配规则，例如：${test} 匹配后为：test
# variable_regex_compile = re.compile(r"\$\{(\w+)\}|\$(\w+)")
# # 匹配规则，例如：${func(${var_1}, ${var_2})}
# function_regex_compile = re.compile(r"\$\{(\w+)\(([\$\w\.\-/\s=,]*)\)\}")
# 提取的断言元素
session_variables_mapping = {}
# 获取的config设置内容
all_veriables_mapping = {}
res_list = []


class Runapi:
    def __init__(self):
        self.action = ParseContent(all_veriables_mapping)

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
        global res_list
        # 有config时执行以下代码
        if all_veriables_mapping["config"]:
            try:
                base_url = all_veriables_mapping["config"]["base_url"]
                if len(base_url) < len(request["url"]):
                    request["url"] = request["url"]
                else:
                    request["url"] = base_url + "/" + request["url"]
            except KeyError:
                request["url"] = request["url"]
            variables = all_veriables_mapping["config"].get("variables", None)
            if variables is not None:
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
                        parsed_validate = self.action.parse_content(api_info["validate"],
                                                                    parsed_config)  # 解析断言部分validate是否有替换的参数,如：${}
                        try:
                            """判断是否有设置verify，绕过ssl验证"""
                            verify = all_veriables_mapping["config"]["verify"]
                            parsed_request["verify"] = verify
                        except KeyError:
                            pass
                        result_data = self.send_request(parsed_validate, parsed_request, api_info, csv_dict)
                        res_list.append(result_data)
                    return res_list

                else:
                    """
                        config中的variables变量的key直接输入的，执行以下方法，类似：
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
                    result_data = self.send_request(api_info["validate"], parsed_request, api_info)
                    res_list.append(result_data)
                    return res_list
        else:
            parsed_request = self.action.parse_content(request, session_variables_mapping)
            result_data = self.send_request(api_info["validate"], parsed_request, api_info)
            res_list.append(result_data)
            return res_list

    def send_request(self, validate=None, parsed_request=None, api_info=None, csv_dict=None):
        """发送请求"""
        method = parsed_request.pop("method")
        url = parsed_request.pop("url")
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        reps = session.request(method, url, **parsed_request)
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "cookies.yaml")
        # if api_info.get("save"):
        #     Utils.write_data_to_yaml(path, {"cookies": {"cookies": api_info.get("save")}})
        if csv_dict:
            result_data = self.action.parse_return_info(validate, reps, url,
                                                        method, parsed_request,
                                                        api_info, api_info["name"], csv_dict.get("desc"))
        else:
            result_data = self.action.parse_return_info(validate, reps, url,
                                                        method, parsed_request,
                                                        api_info, api_info["name"])

        self.extract_data(api_info, reps)
        if api_info.get("save"):
            parsed_save = self.action.parse_content(api_info["save"], session_variables_mapping)
            save_dict = {"cookies":{"cookie": parsed_save}}
            Utils.write_data_to_yaml(path, save_dict)
        return result_data

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
            var_value = Utils.extract_json_field(reps, var_expr)
            session_variables_mapping[var_name] = var_value




if __name__ == '__main__':
    str_1 = "xxxs:${test_1($username,$password)}ssss:wwwww"
    test_dict = {"username": "zhangsan", "password": 123456, "age": 21}
    print(Runapi().action.parse_funtion(str_1, test_dict))
