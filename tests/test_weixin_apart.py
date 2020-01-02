
from htturunner.result_assert import Result


class TestApart:

    def test_get_department_token(self):
        """获取token"""
        Result.result_assert("api", "get_weixin_tocken.yml")

    def test_get_department_list(self):
        """获取部门列表"""
        Result.result_assert("api", "get_department_list.yml")

    def test_create_department(self):
        """创建部门"""
        Result.result_assert("api", "get_create_department.yml")
