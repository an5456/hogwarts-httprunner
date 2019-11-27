import re

import jsonpath
import urllib3
from requests import sessions
import os
from htturunner.loader import load_yml
from htturunner.validate import is_api, is_testcase
import warnings

session = sessions.Session()
variable_regex_compile = re.compile(r".*\$(\w+).*")
session_variables_mapping = {}
all_veriables_mapping = {}


def extract_json_field(resp, json_field):
    value = jsonpath.jsonpath(resp.json(), json_field)
    return value[0]


def replace_var(content, variables_mapping):
    matched = variable_regex_compile.match(content)
    if not matched:
        return content

    var_name = matched[1]
    value = variables_mapping[var_name]
    replace_content = content.replace("${}".format(var_name), str(value))
    return replace_content


def parse_content(content, variables_mapping):
    if isinstance(content, dict):
        parsed_content = {}
        for key, value in content.items():
            parsed_value = parse_content(value, variables_mapping)
            parsed_content[key] = parsed_value
        return parsed_content
    elif isinstance(content, list):
        parsed_content = []
        for item in content:
            parsed_item = parse_content(item, variables_mapping)
            parsed_content.append(parsed_item)
        return parsed_content
    elif isinstance(content, str):
        matched = variable_regex_compile.match(content)
        if matched:
            return replace_var(content, variables_mapping)
        else:
            return content
    else:
        return content


def run_api(api_info):
    """

    :param api:
        {
            "request": {},
            "validate": {}
        }
    :return:

    """
    warnings.simplefilter("ignore", ResourceWarning)
    get_run_api(api_info)
    request = api_info["request"]
    global session_variables_mapping
    # parsed_request = parse_content(request, session_variables_mapping)
    # method = parsed_request.pop("method")
    if all_veriables_mapping["config"]:
        base_url = all_veriables_mapping["config"]["base_url"]
        request["url"] = base_url + "/" + request["url"]
        verify = all_veriables_mapping["config"]["verify"]
        parsed_request = parse_content(request, session_variables_mapping)
        parsed_request["verify"] = verify
        method = parsed_request.pop("method")
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        url = parsed_request.pop("url")
        reps = session.request(method, url, **parsed_request)
    else:
        parsed_request = parse_content(request, session_variables_mapping)
        method = parsed_request.pop("method")
        url = parsed_request.pop("url")
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        reps = session.request(method, url, **parsed_request)
    # requests 每一次调用都会创建一个session，所以用同一个session访问
    # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    # reps = session.request(method, url, **parsed_request)
    # 响应断言如果断言的key里面有"$"就用jsonpath获取断言的结果
    # 如果没有"$"就用一般的json规则去提取数据
    validator_mapping = api_info["validate"]
    for key in validator_mapping:
        if "$" in key:
            actual_value = extract_json_field(reps, key)
        else:
            actual_value = getattr(reps, key)  # 实际结果
        expected_value = validator_mapping[key]  # 预期结果
        assert actual_value == expected_value
    # 提取响应参数
    extract_mapping = api_info.get("extract", {})
    for var_name in extract_mapping.keys():
        var_expr = extract_mapping[var_name]
        var_value = extract_json_field(reps, var_expr)
        session_variables_mapping[var_name] = var_value

    return True


# def run_api_yaml(yml_file):
#     load_json = load_yml(yml_file)
#     return run_api(load_json)
#
#
# def run_testcse_yml(testcase_yml_file):
#     load_api_list = load_yml(testcase_yml_file)
#     for api_info in load_api_list:
#         run_api(api_info)


def run_yml(yml_file):
    """运行yml文件"""
    result = []
    load_content = load_yml(yml_file)
    global all_veriables_mapping
    all_veriables_mapping["config"] = load_content.get("config", {})

    if is_api(load_content.get("teststeps")):
        success = run_api(load_content)
        result.append(success)
    elif is_testcase(load_content.get("teststeps")):
        for api_info in load_content.get("teststeps"):
            success = run_api(api_info)
            result.append(success)
    else:
        raise Exception("YAML format invalid".format(yml_file))

    return result


def load_veritable(yml_file):
    load_content = load_yml(yml_file)
    return load_content


# 获取依赖接口
def get_run_api(api_info):
    file_path = os.path.dirname(os.path.dirname(__file__)) + "/tests/"
    if api_info.get("api"):
        ru_path = os.path.join(file_path, api_info.get("api"))
        print("依赖运行了")
        load_veritable(ru_path)
        run_yml(ru_path)


def get_config(api_info):
    file_path = os.path.dirname(os.path.dirname(__file__)) + "/tests/"
    if api_info.get("api"):
        ru_path = os.path.join(file_path, api_info.get("api"))
        print("依赖运行了")
        load_veritable(ru_path)


# def load_veriables(api_info):
#     file_path = os.path.dirname(os.path.dirname(__file__)) + "/tests/"
#     if api_info.get("base_url" ):
#         pass

if __name__ == '__main__':
    get_run_api({"api": "api/get_login.yml"})
