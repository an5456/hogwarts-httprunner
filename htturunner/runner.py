import csv
import io
import re
from json import JSONDecodeError
import jsonpath
import urllib3
from requests import sessions
import os
from htturunner.loader import load_yml
from htturunner.validate import is_api, is_testcase
import warnings
import sys
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(BASE_DIR)

session = sessions.Session()
# 匹配规则，例如：${test} 匹配后为：test
variable_regex_compile = re.compile(r"\$\{(\w+)\}|\$(\w+)")
# 提取的断言元素
session_variables_mapping = {}
# 获取的config设置内容
all_veriables_mapping = {}


# 对应接口返回的json响应内容，使用jsonpath 提取想要的字段
def extract_json_field(resp, json_field):
    value = jsonpath.jsonpath(resp.json(), json_field)
    return value[0]


# 字段替换
def replace_var(content, variables_mapping):
    try:
        vars_list = []
        for var_tuple in variable_regex_compile.findall(content):
            vars_list.append(
                var_tuple[0] or var_tuple[1]
            )
    except TypeError:
        return []
    if not vars_list:
        return content

    var_name = vars_list
    # 同一行字符串替换两个字段
    if 1 < len(var_name) <= 2:
        value = variables_mapping[var_name[0]]
        value1 = variables_mapping[var_name[1]]
        replace_content = content.replace("${%s}" % var_name[0], str(value)).replace("${%s}" % var_name[1], str(value1))
    # 同一行字符串，替换三个字段
    elif len(var_name) > 2:
        value = variables_mapping[var_name[0]]
        value1 = variables_mapping[var_name[1]]
        value2 = variables_mapping[var_name[2]]
        replace_content = content.replace("${%s}" % var_name[0], str(value)).replace("${%s}" % var_name[1],
                                                                                     str(value1)).replace(
            "${%s}" % var_name[2], str(value2))
    else:
        value = variables_mapping[var_name[0]]
        replace_content = content.replace("${%s}" % var_name[0], str(value))
    return replace_content


# 解析请求是否含有类似${},如果有就替换
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
        matched = variable_regex_compile.findall(content)
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

        if len(base_url) < len(request["url"]):
            request["url"] = request["url"]
        else:
            request["url"] = base_url + "/" + request["url"]

        variables = all_veriables_mapping["config"]["variables"]

        if variables is not None:
            csv_request = api_info
            for key, value in variables.items():
                session_variables_mapping[key] = value
            if "$" in str(variables):
                csv_info = load_csv()
                for csv_dict in csv_info:
                    parsed_config = parse_content(variables, csv_dict)
                    parsed_request = parse_content(request, parsed_config)
                    variables_request = parse_content(csv_request, parsed_config)
                    try:
                        verify = all_veriables_mapping["config"]["verify"]
                        parsed_request["verify"] = verify
                    except KeyError:
                        pass
                    method = parsed_request.pop("method")
                    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                    url = parsed_request.pop("url")
                    print(url)
                    reps = session.request(method, url, **parsed_request)
                    validator_mapping = variables_request["validate"]
                    for key in validator_mapping:
                        if "$" in key:
                            actual_value = str(extract_json_field(reps, key))
                        else:
                            actual_value = getattr(reps, key)  # 实际结果
                        expected_value = validator_mapping[key]  # 预期结果
                        try:
                            if isinstance(actual_value, int) or isinstance(expected_value, int):
                                actual_value = int(actual_value)
                                expected_value = int(expected_value)
                                assert actual_value == expected_value
                            else:
                                assert actual_value == expected_value
                        except AssertionError:
                            print("=======断言错误=====")
                            print("expected:{}".format(expected_value))
                            print("actual:{}".format(actual_value))
                    try:
                        info = reps.json()
                        print(info)
                    except JSONDecodeError:
                        print(reps)
            else:
                parsed_request = parse_content(request, session_variables_mapping)
                try:
                    verify = all_veriables_mapping["config"]["verify"]
                    parsed_request["verify"] = verify
                except KeyError:
                    pass
                method = parsed_request.pop("method")
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
                url = parsed_request.pop("url")
                print(url)
                reps = session.request(method, url, **parsed_request)
                try:
                    info = reps.json()
                    print(info)
                except JSONDecodeError:
                    print(reps)
    else:
        parsed_request = parse_content(request, session_variables_mapping)
        method = parsed_request.pop("method")
        url = parsed_request.pop("url")
        print(url)
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        reps = session.request(method, url, **parsed_request)
        try:
            info = reps.json()
            print(info)
        except JSONDecodeError:
            print(reps)
    # requests 每一次调用都会创建一个session，所以用同一个session访问
    # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    # reps = session.request(method, url, **parsed_request)
    # 响应断言如果断言的key里面有"$"就用jsonpath获取断言的结果
    # 如果没有"$"就用一般的json规则去提取数据
    # validator_mapping = api_info["validate"]
    # for key in validator_mapping:
    #     if "$" in key:
    #         actual_value = extract_json_field(reps, key)
    #     else:
    #         actual_value = getattr(reps, key)  # 实际结果
    #     expected_value = validator_mapping[key]  # 预期结果
    #     assert actual_value == expected_value
    # 提取响应参数
    extract_mapping = api_info.get("extract", {})
    for var_name in extract_mapping.keys():
        var_expr = extract_mapping[var_name]
        var_value = extract_json_field(reps, var_expr)
        session_variables_mapping[var_name] = var_value

    return True





def run_yml(yml_file):
    """运行yml文件"""
    result = []
    load_content = load_yml(yml_file)
    global all_veriables_mapping
    all_veriables_mapping["config"] = load_content.get("config", {})

    if is_api(load_content.get("teststeps")):
        success = run_api(load_content.get("teststeps"))
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


# def get_config(api_info):
#     file_path = os.path.dirname(os.path.dirname(__file__)) + "/tests/"
#     if api_info.get("api"):
#         ru_path = os.path.join(file_path, api_info.get("api"))
#         print("依赖运行了")
#         load_veritable(ru_path)


# def load_veriables(api_info):
#     file_path = os.path.dirname(os.path.dirname(__file__)) + "/tests/"
#     if api_info.get("base_url" ):
#         pass
def load_csv():
    csv_file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    path = os.path.join(csv_file_path+"/tests/data/", "login.csv")
    print(path)
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


if __name__ == '__main__':
    l = load_csv()
    print(l)





