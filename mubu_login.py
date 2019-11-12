import requests
import urllib3
import unittest
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class TestMuBuLogin(unittest.TestCase):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def test_get_home_page(self):
        url = "https://mubu.com/"
        method = "GET"
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/78.0.3904.97 Safari/537.36 "
        }
        kwargs = {
            "headers": headers,
            "verify": False
        }
        res = requests.request(method, url, **kwargs)
        print(res.status_code)
        assert res.status_code == 200

    def test_get_login(self):
        url = "https://mubu.com/login"
        method = "GET"
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/78.0.3904.97 Safari/537.36 "
        }
        kwargs = {
            "headers": headers,
            "verify": False
        }
        res = requests.request(method, url, **kwargs)
        print(res.status_code)
        assert res.status_code == 200

    def test_get_login_password(self):
        url = "https://mubu.com/login/password"
        method = "GET"
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/78.0.3904.97 Safari/537.36 "
        }
        kwargs = {
            "headers": headers,
            "verify": False
        }
        res = requests.request(method, url, **kwargs)
        print(res.status_code)
        assert res.status_code == 200

    def test_post_login(self):
        url = "https://mubu.com/api/login/submit"
        method = "POST"
        headers = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/78.0.3904.97 Safari/537.36 ",
            "content-type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        data = {
            "phone": "17729597958",
            "password": "dong19871103",
            "remember": "true"

        }
        kwargs = {
            "headers": headers,
            "data": data,
            "verify": False
        }
        res = requests.request(method, url, **kwargs)
        print(res.json())
        assert res.status_code == 200
        assert res.json()["code"] == 0



