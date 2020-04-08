# import re
#
# dolloar_regex_compile = re.compile(r"\$\$")
# # variable notation, e.g. ${var} or $var
# variable_regex_compile = re.compile(r"\$\{(\w+)\}|\$(\w+)")
# # function notation, e.g. ${func1($var_1, $var_3)}
# function_regex_compile = re.compile(r"\$\{(\w+)\(([\$\w\.\-/\s=,]*)\)\}")
#
# def is_var_or_func_exist(content):
#     """ check if variable or function exist
#     """
#     # if not isinstance(content, basestring):
#     #     return False
#
#     try:
#         match_start_position = content.index("$", 0)
#     except ValueError:
#         return False
#
#     while match_start_position < len(content):
#         dollar_match = dolloar_regex_compile.match(content, match_start_position)
#         if dollar_match:
#             match_start_position = dollar_match.end()
#             continue
#
#         func_match = function_regex_compile.match(content, match_start_position)
#         if func_match:
#             return True
#
#         var_match = variable_regex_compile.match(content, match_start_position)
#         if var_match:
#             print(var_match)
#             return True
#
#         return False
#
#
# # print(is_var_or_func_exist("jfdlsafjkl$code$test"))
# def regex_findall_variables(content):
#     """ extract all variable names from content, which is in format $variable
#
#     Args:
#         content (str): string content
#
#     Returns:
#         list: variables list extracted from string content
#
#     # Examples:
#     #     >>> regex_findall_variables("$variable")
#     #     ["variable"]
#     #
#     #     >>> regex_findall_variables("/blog/$postid")
#     #     ["postid"]
#     #
#     #     >>> regex_findall_variables("/$var1/$var2")
#     #     ["var1", "var2"]
#     #
#     #     >>> regex_findall_variables("abc")
#     #     []
#
#     """
#     try:
#         vars_list = []
#         for var_tuple in variable_regex_compile.findall(content):
#             vars_list.append(
#                 var_tuple[0] or var_tuple[1]
#             )
#         return vars_list
#     except TypeError:
#         return []
#
#
# print(regex_findall_variables("fds${afd}sfdsfadsaf$tests$gggg")[2])
# from selenium import webdriver
# import time
# firefox_capabilities = {
#     "browserName": "chrome",
#     "version": "",  # 注意版本号一定要写对
#     "platform": "ANY",
#     "javascriptEnabled": True,
#     "marionette": True,
# }
# browser = webdriver.Remote("http://127.0.0.1:5001/wd/hub",
#                            desired_capabilities=firefox_capabilities)  # 注意端口号4444是我们上文中映射的宿主机端口号
# browser.get("http://www.baidu.com")
# # browser.get_screenshot_as_file(r"C:/baidu.png")
# browser.maximize_window()
# time.sleep(5)
# browser.close()

# export WORKON_HOME=/usr/local/my_env
# export VIRTUALENVWRAPPER_PYTHON=/usr/local/python3/bin/python3
# source /Library/Frameworks/Python.framework/Versions/3.6/bin/virtualenvwrapper.sh
# PATH="/Library/Frameworks/Python.framework/Versions/3.6/bin:${PATH}"
# export PATH
# import subprocess
# res = subprocess.run("nohup python3 -m http.server >out.log 2>&1 & ", shell=True)
# a = "432432432423hhh"
# a.replace(a, "123213213")
# print(a)
import sys
class Person(object):
    pass
p = Person()
p1 = p
print(sys.getrefcount(p))
p2 = p1
print(sys.getrefcount(p))
p3 = p2
print(sys.getrefcount(p))
del p1
print(sys.getrefcount(p))
