import pytest


@pytest.fixture(scope='module', autouse=True)
def params():
    info = "hello world"
    cookies = get_cookies()
    yield cookies
    print("测试之用运行的方法")


def get_cookies():
   return 4