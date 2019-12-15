import unittest

from htturunner.runner import replace_var


# class TestHogRunner(unittest.TestCase):
#     def test_replace_var(self):
#         raw_str = "https://mubu.com/list?code=$code"
#         variables_mapping = {
#             "code": 0
#         }
#         replace_str = replace_var(raw_str, variables_mapping)
#         self.assertEqual(replace_str, "https://mubu.com/list?code=0")
#
#     def __getitem__(self):
#         print(self.__dict__)
import tests.testcase