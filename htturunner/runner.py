import re

import jsonpath
from requests import sessions

from htturunner.loader import load_yml
from htturunner.validate import is_api, is_testcase

session = sessions.Session()
variable_regex_compile = re.compile(r".*\$(\w+).*")
session_variables_mapping = {}


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
    request = api_info["request"]
    global session_variables_mapping
    parsed_request = parse_content(request, session_variables_mapping)
    method = parsed_request.pop("method")
    url = parsed_request.pop("url")
    print(url)
    # requests 每一次调用都会创建一个session，所以用同一个session访问
    reps = session.request(method, url, **parsed_request)
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
        print('====' + str(var_value))
    print(run_api)
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
    if is_api(load_content):
        success = run_api(load_content)
        result.append(success)
    elif is_testcase(load_content):
        for api_info in load_content:
            success = run_api(api_info)
            result.append(success)
    else:
        raise Exception("YAML format invalid".format(yml_file))
    print("=======" + str(result))
    return result
