import re
from htturunner.func_suit import FuncSuit

# 匹配规则，例如：${test} 匹配后为：test

from htturunner.validate import is_api

variable_regex_compile = re.compile(r"\$\{(\w+)\}|\$(\w+)")
# 匹配规则，例如：${func(${var_1}, ${var_2})}
function_regex_compile = re.compile(r"\$\{(\w+)\(([\$\w\.\-/\s=,]*)\)\}")

# 提取的断言元素
session_variables_mapping = {}


# 获取的config设置内容
# all_veriables_mapping = {}


class ParseContent:
    def __init__(self, all_veriables_mapping):
        self.all_veriables_mapping = all_veriables_mapping

    def parse_content(self, content, variables_mapping):
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
        print(type(f))
        if info_dict:
            if fun_name in f:
                return f[fun_name](FuncSuit(), **info_dict)
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
                for i in regx_data:
                    if "$" in i[1]:
                        for re_data in variable_regex_compile.findall(i[1]):
                            parse_list.append(re_data[0] or re_data[1])
                        for value in parse_list:
                            try:
                                result_dict[value] = info_dict[value]
                            except Exception as e:
                                print(e)
                        ret = str_1.replace("${%s($%s,$%s)}" % (regx_data[0][0], parse_list[0], parse_list[1]),
                                            self.res(regx_data[0][0], result_dict))
                        return ret
                    else:
                        return str_1.replace("${%s()}" % (regx_data[0][0]), self.res(regx_data[0][0]))
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