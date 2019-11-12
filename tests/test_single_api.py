import os
import unittest

import yaml

from hogwars_httprunner.loader import load_yml
from hogwars_httprunner.runner import run_yaml


class TestSingleApi(unittest.TestCase):
    """加载出的接口请求参数与原始信息一样"""
    def test_loader_single_api(self):
        single_api_yaml = os.path.join(os.path.dirname(__file__), "api", "get_home_page.yml")
        loaaded_json = load_yml(single_api_yaml)
        self.assertEqual(loaaded_json["request"]["url"], "https://mubu.com/")
        # self.assertEqual(loaaded_json["verify"], False)

    def test_run_single_yaml(self):
        single_api_yaml = os.path.join(os.path.dirname(__file__), "api", "get_home_page.yml")
        result = run_yaml(single_api_yaml)
        print(result)
        self.assertEqual(result, True)

        single_api_yaml = os.path.join(os.path.dirname(__file__), "api", "get_login.yml")
        result = run_yaml(single_api_yaml)
        print(result)
        self.assertEqual(result, True)

        single_api_yaml = os.path.join(os.path.dirname(__file__), "api", "get_login_submit.yml")
        result = run_yaml(single_api_yaml)
        print(result)
        self.assertEqual(result, True)


