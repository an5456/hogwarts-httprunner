import json
import re
import jsonpath
import yaml
from lxml import etree


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
        try:
            if isinstance(resp, dict):
                value = jsonpath.jsonpath(resp, json_field)
            elif "html" in resp.text:
                html = etree.HTML(resp.text, etree.HTMLParser())
                value = html.xpath(json_field+'//text()')
            else:
                value = jsonpath.jsonpath(resp.json(), json_field)
            return value[0]
        except IndexError:
            return value

    @classmethod
    def write_data_to_yaml(cls, path, data):
        """写入数据到yaml文件"""
        operation = open(path, 'w', encoding='utf-8')
        yaml.dump(data, operation)

    @classmethod
    def read_yaml(cls, path):
        """读取yaml中信息"""
        operation = open(path, "r", encoding="utf-8")
        return yaml.load(operation.read(), Loader=yaml.FullLoader)


if __name__ == '__main__':
    s = Utils()
    data = {"cookies": {"cookie": "HSX9fJjjCIImOJoPUkv/QA=="}}
    # s.write_data_to_yaml("/Users/anxiaodong/PycharmProjects/hogwarts-httprun/data/cookies.yaml", data)

    print(s.read_yaml("/Users/anxiaodong/PycharmProjects/hogwarts-httprun/data/env.yml"))
