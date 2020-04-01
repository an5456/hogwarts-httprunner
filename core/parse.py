import re
from json import JSONDecodeError

from requests_toolbelt import MultipartEncoder

from core.func_suit import FuncSuit

# 匹配规则，例如：${test} 匹配后为：test
from core.utis import Utils

variable_regex_compile = re.compile(r"\$\{(\w+)\}|\$(\w+)")
# 匹配规则，例如：${func(${var_1}, ${var_2})}
function_regex_compile = re.compile(r"\$\{(\w+)\(([\$\w\.\-/\s=,]*)\)\}")

# 提取的断言元素
session_variables_mapping = {}


class ParseContent:
    def __init__(self, all_veriables_mapping):
        self.all_veriables_mapping = all_veriables_mapping

    def parse_content(self, content, variables_mapping):
        """解析和替换"""
        if isinstance(content, dict):
            parsed_content = {}
            for key, value in content.items():
                parsed_value = self.parse_content(value, variables_mapping)
                parsed_content[key] = parsed_value
            return parsed_content
        elif isinstance(content, list):
            parsed_content = []
            for item in content:
                parsed_item = self.parse_content(item, variables_mapping)
                parsed_content.append(parsed_item)
            return parsed_content
        elif isinstance(content, str):
            matched = variable_regex_compile.findall(content)
            matched_function = function_regex_compile.findall(content)

            if matched_function:
                return self.parse_funtion(content, self.all_veriables_mapping["config"].get("variables"))

            elif matched:
                return self.replace_var(content, variables_mapping)
            else:
                return content

        else:
            return content

    # 获取模块中的类的方法名，并执行
    def res(self, fun_name, info_dict=None):
        f = FuncSuit.__dict__
        if info_dict:
            if fun_name in f:
                return f[fun_name](FuncSuit(), info_dict)
            else:
                print(fun_name+"不存在")
        else:
            if fun_name in f:
                return f[fun_name](FuncSuit())

    def parse_funtion(self, str_1, info_dict):
        """
        :param str_1: 需要解析的字符串 类似：https://mubu.com/${test_2()}
        :param info_dict: 需要替换的数据
        :return: 被替换后的字符串 ，类似：https://mubu.com/17729678
        """
        result_dict = {}
        parse_list = []
        regx_data = function_regex_compile.findall(str_1)
        try:
            if regx_data:
                    if regx_data[0][1] is not "":
                            if "$" in regx_data[0][1]:
                                for re_data in variable_regex_compile.findall(regx_data[0][1]):
                                    parse_list.append(re_data[0] or re_data[1])
                                for value in parse_list:
                                    try:
                                        result_dict[value] = info_dict[value]
                                    except Exception as e:
                                        print(e)
                                s = "${%s($%s,$%s)}" % (regx_data[0][0], parse_list[0], parse_list[1])
                                print(s)
                                r = self.res(regx_data[0][0], result_dict)
                                print(r)
                                return str_1.replace("${%s($%s,$%s)}" % (regx_data[0][0], parse_list[0], parse_list[1]), str_1.replace(str(s), str(r)))
                            else:
                                t = regx_data[0][1].split(",")
                                result_dict[t[0]] = t[0]
                                result_dict[t[1]] = t[1]
                                g = "${%s(%s,%s)}" % (regx_data[0][0], t[0], t[1])
                                return str_1.replace("${%s(%s,%s)}" % (regx_data[0][0], t[0], t[1]), self.res(regx_data[0][0], t))
                    else:
                        return str_1.replace("${%s()}" % (regx_data[0][0]), str(self.res(regx_data[0][0])))
        except Exception as e:
            print("=====" + str(e))

    # 字段替换
    def replace_var(self, content, variables_mapping):
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
            replace_content = content.replace("${%s}" % var_name[0], str(value)).replace("${%s}" % var_name[1],
                                                                                         str(value1))
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

    def parse_return_info(self, variables_request, reps, url, method, parsed_request, api_info, name, session_mapping_dict, csv_dict=None, ):
        """组装返回断言和日志信息"""
        if isinstance(parsed_request.get("data"), MultipartEncoder):
            # parsed_request["data"] = session_mapping_dict
            parsed_request.pop("data")
            parsed_request["upfile"] = session_mapping_dict["upfile"]

        variables_request = self.parse_content(variables_request, session_mapping_dict)
        exp = []
        for var_value in variables_request:
            for key, value in var_value.items():
                if "eq" in key:
                    key = value[0]
                    # 响应断言如果断言的key里面有"$"就用jsonpath获取断言的结果
                    # 如果没有"$"就用一般的json规则去提取数据
                    if "content" in key:
                        key = key.replace("content", "$")

                    if "$" in key:
                        if len(value) > 2:
                            actual_value = str(Utils.extract_json_field(session_mapping_dict, key))
                        else:
                            actual_value = str(Utils.extract_json_field(reps, key))
                    else:
                        actual_value = str(getattr(reps, key))  # 实际结果
                    expected_value = value[1]  # 预期结果

                    if isinstance(actual_value, int) or isinstance(expected_value, int):
                        if actual_value == 'False' or actual_value == 'True':
                            actual_value = actual_value
                        else:
                            actual_value = int(actual_value)
                        expected_value = int(expected_value)
                    reps_dict = {
                        "expected": expected_value,
                        "actual": actual_value,
                        "key": key
                    }
                    exp.append(reps_dict)
        try:
            reps = reps.json()
        except JSONDecodeError:
            # reps = reps.text
            reps = ""
        res_dict = {
            "name": name,
            "csv_name": csv_dict,
            "url": url,
            "method": method,
            "request_data": {**parsed_request},
            "response_data": reps,
            "assert_data": exp,
            "request_info": api_info
        }

        return res_dict
