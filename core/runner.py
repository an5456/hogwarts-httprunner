import base64
import json
import urllib3
from requests import sessions
import os

from core.loader import Load
from core.parse import ParseContent
from core.utis import Utils
from core.validate import is_api, is_testcase
import warnings
import logging
from requests_toolbelt.multipart.encoder import MultipartEncoder
session = sessions.Session()
# # 匹配规则，例如：${test} 匹配后为：test
# variable_regex_compile = re.compile(r"\$\{(\w+)\}|\$(\w+)")
# # 匹配规则，例如：${func(${var_1}, ${var_2})}
# function_regex_compile = re.compile(r"\$\{(\w+)\(([\$\w\.\-/\s=,]*)\)\}")
# 提取的断言元素
session_variables_mapping = {}
# 获取的config设置内容
all_veriables_mapping = {}


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
        res_list = []
        global session_variables_mapping

        warnings.simplefilter("ignore", ResourceWarning)
        self.get_run_api(api_info)  # 判断是否获取依赖接口
        request = api_info["request"]
        if request.get("upfile"):
            up_data = request.get("upfile")
            multipart_encoder = MultipartEncoder(
                fields={
                    up_data["fileType"]: (up_data["fileName"], open(up_data["filePath"], 'rb'))
                }
            )
            request["data"] = multipart_encoder
            request["headers"]["Content-Type"] = multipart_encoder.content_type
            session_variables_mapping["upfile"] = request.pop("upfile")

        # 有config时执行以下代码
        if all_veriables_mapping["config"]:
            try:
                base_url = all_veriables_mapping["config"]["base_url"]
                if base_url:
                    if len(base_url) < len(request["url"]):
                        request["url"] = request["url"]
                    else:
                        request["url"] = base_url + "/" + request["url"]
            except KeyError:
                request["url"] = request["url"]
            variables = all_veriables_mapping["config"].get("variables")

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
                # 没有config时发送请求
                return self.not_config_send_request(request, api_info)
        else:
            return self.not_config_send_request(request, api_info)

    def run_yml(self, yml_file):
        """运行yml文件"""
        result = []
        end_result = []
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
        end_result.append(result)
        return end_result

    # 获取依赖接口
    def get_run_api(self, api_info):
        file_path = os.path.dirname(os.path.dirname(__file__)) + "/tests/"
        if api_info.get("api"):
            ru_path = os.path.join(file_path, api_info.get("api"))
            print("依赖运行了")
            Load.load_yml(ru_path)
            self.run_yml(ru_path)

    def teardown_yaml(self, api_info):
        """断言依赖其它接口的返回值"""
        file_path = os.path.dirname(os.path.dirname(__file__)) + "/tests/"
        if api_info["teardown"].get("api"):
            ru_path = os.path.join(file_path, api_info["teardown"].get("api"))
            Load.load_yml(ru_path)
            self.run_yml(ru_path)

    def get_request_data(self, parsed_request, api_info):
        """获取请求数据"""
        parsed_request = self.action.parse_content(parsed_request, session_variables_mapping)
        try:
            extract_mapping = api_info.get("extr", {})
            for var_name in extract_mapping.keys():
                var_expr = extract_mapping[var_name]
                var_value = Utils.extract_json_field(parsed_request, var_expr)
                session_variables_mapping[var_name] = var_value
        except Exception as e:
            logging.error(e)

    def extract_data(self, api_info, reps):
        """提取响应断言信息"""
        extract_mapping = api_info.get("extract", {})
        try:
            for var_name in extract_mapping.keys():
                var_expr = extract_mapping[var_name]
                if "${" in var_expr or "$" in var_expr:
                    var_expr = self.action.parse_content(var_expr, session_variables_mapping)
                    if "$" in var_expr:
                        var_value = Utils.extract_json_field(reps, var_expr)
                    else:
                        var_value = var_expr
                    session_variables_mapping[var_name] = var_value
        except AttributeError:
            logging.error("extract is None")

    def send_request(self, parsed_validate, parsed_request, api_info, csv_dict=None):
        """发送请求"""
        config_info = Utils.read_yaml(os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "env.yml"))
        if config_info:
            if config_info["weixin"]["schema"] is not None:
                if config_info["weixin"]["schema"] == "http":  # 是否是http请求
                    url = parsed_request.pop("url").replace("qyapi.weixin.qq.com",
                                                            config_info["weixin"]["qyapi.weixin.qq.com"][
                                                                config_info["weixin"]["default"]])
                    method = parsed_request.pop("method")
                    parsed_request["headers"]["Host"] = "qyapi.weixin.qq.com"
                    if api_info.get('teardown'):
                        session_variables_mapping["extract"] = api_info['teardown'].get("extract")
                    else:
                        if session_variables_mapping.get("extract"):
                            api_info["extract"] = session_variables_mapping["extract"]
                    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                    reps = session.request(method, url, **parsed_request)
                    if api_info.get("encoding") is not None:
                        if api_info["encoding"] == "base64":  # 是否加密
                            reps = json.loads(base64.b64decode(reps.content))
                    self.get_request_data(parsed_request, api_info)
                    self.extract_data(api_info, reps)
                    return self.extract_and_get_data(parsed_validate, parsed_request, api_info, csv_dict, reps, url,
                                                     method)
                elif "dubbo" == config_info["schema"]:
                    pass
                elif "websocket" == config_info["schema"]:
                    pass
                elif "urllib" == config_info['schema']:
                    pass
                else:
                    pass
        else:
            method = parsed_request.pop("method")
            url = parsed_request.pop("url")

            if api_info.get('teardown'):
                session_variables_mapping["extract"] = api_info['teardown'].get("extract")
            else:
                if session_variables_mapping.get("extract"):
                    api_info["extract"] = session_variables_mapping["extract"]
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            reps = session.request(method, url, **parsed_request)

            self.get_request_data(parsed_request, api_info)
            self.extract_data(api_info, reps)
            return self.extract_and_get_data(parsed_validate, parsed_request, api_info, csv_dict, reps, url, method)

    def extract_and_get_data(self, parsed_validate, parsed_request, api_info, csv_dict, reps, url, method):
        """提取请求或者响应的数据，已经保存数据到yml文件"""

        try:
            self.teardown_yaml(api_info)
            if session_variables_mapping.get("extract") is not None:
                session_variables_mapping.pop("extract")

        except KeyError:
            pass

        if csv_dict:
            result_data = self.action.parse_return_info(parsed_validate, reps, url,
                                                        method, parsed_request,
                                                        api_info, api_info["name"],
                                                        session_variables_mapping,
                                                        csv_dict.get("desc"))
        else:
            result_data = self.action.parse_return_info(parsed_validate, reps, url,
                                                        method, parsed_request,
                                                        api_info, api_info["name"],
                                                        session_variables_mapping)
        path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "cookies.yaml")
        if api_info.get("save"):
            parsed_save = self.action.parse_content(api_info["save"], session_variables_mapping)
            save_dict = {"cookies": {"cookie": parsed_save}}
            Utils.write_data_to_yaml(path, save_dict)
        return result_data

    def not_config_send_request(self, request, api_info):
        """没有config时发送请求"""
        res_list = []
        parsed_request = self.action.parse_content(request, session_variables_mapping)
        try:
            """判断是否有设置verify，绕过ssl验证"""
            verify = all_veriables_mapping["config"]["verify"]
            parsed_request["verify"] = verify
        except KeyError:
            pass
        result_data = self.send_request(api_info["validate"], parsed_request, api_info)
        res_list.append(result_data)
        return res_list
    def upload_file(self):
        multipart_encoder = MultipartEncoder(
            fields={
                'file': ('customerTemp.xlsx', open('D:\模板\customerTemp.xlsx', 'rb'), 'file/xlsx')
            }
        )
        headers = {
            "Content-Type": multipart_encoder.content_type
        }


if __name__ == '__main__':
    str_1 = "xxxs:${test_1($username,$password)}ssss:wwwww"
    test_dict = {"username": "zhangsan", "password": 123456, "age": 21}
    print(Runapi().action.parse_funtion(str_1, test_dict))
