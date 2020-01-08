import allure
from main_function.result_assert import Result


@allure.feature("部门管理")
class TestApart:
    @allure.story("001获取tocken")
    def setup_class(self):
        """001获取token"""
        Result.result_assert("api/base_api", "get_weixin_token.yml")

    @allure.story("002获取部分列表")
    def test_get_department_list(self):
        """获取部门列表"""
        Result.result_assert(filename="get_department_list.yml")

    @allure.story("003创建部门")
    def test_create_department(self):
        """创建部门"""
        Result.result_assert(filename="get_create_department.yml")

    @allure.story("004修改部门名称")
    def test_update_department(self):
        """修改部门名称"""
        Result.result_assert(filename="get_weixin_update_department.yml")

    @allure.story("005删除部门")
    def test_delete_department(self):
        """删除部门"""
        Result.result_assert(filename="get_weixin_delete_department.yml")
