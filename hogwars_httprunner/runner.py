from hogwars_httprunner.loader import load_yml
import requests


def run_yaml(yml_file):
    load_json = load_yml(yml_file)
    request = load_json["request"]
    method = request.pop("method")
    url = request.pop("url")
    reps = requests.request(method, url, **request)

    validator_mapping = load_json["validate"]
    for key in validator_mapping:
        actual_value = getattr(reps, key)
        expected_value = validator_mapping[key]
        assert actual_value == expected_value
    print(load_json)
    return True
