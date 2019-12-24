import json

import jsonpath


class Utils:
    @classmethod
    def format_output(cls, json_project):
        """信息格式化输出 """
        return json.dumps(json_project, indent=2).encode("utf-8").decode("unicode_escape")

    @classmethod
    def extract_json_field(cls, resp, json_field):
        """
        :param resp: 需要提取的信息
        :param json_field: 解析表达式 $..data
        :return:
        """
        value = jsonpath.jsonpath(resp.json(), json_field)
        return value[0]
