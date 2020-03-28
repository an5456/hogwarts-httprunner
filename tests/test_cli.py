# import os
# import unittest
# import subprocess
#
#
# class TestCli(unittest.TestCase):
#     def test_hogrun_single_yaml(self):
#         single_api_yaml = os.path.join(os.path.dirname(__file__), "api", "get_login_submit.yml")
#         subprocess.run("python -m core.cli {}".format(single_api_yaml))