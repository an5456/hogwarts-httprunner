import pytest

from core.getlog import GetLog


def pytest_configure(config):
    """
        去除 PytestUnknownMarkWarning: Unknown pytest.mark.allure_label.story - is this a typo? 类似这种的警告
        将pytest.mark(allure_label.feature) -is this a typo?,将括号里面的复制到下面的列表中
    """
    marker_list = ["allure_label.story ", "allure_label.feature "]  # allure_label.story
    for markers in marker_list:
        config.addinivalue_line(
            "markers", markers
        )


@pytest.fixture(scope="module", autouse=True)
def get_log():
    GetLog.get_logs_info()

# @pytest.fixture(scope="class", autouse=True)
# def get_weixin_token():
#     Result.result_assert("api/base_api", "get_weixin_token.yml")
