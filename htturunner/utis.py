import json


class Utils:
    @classmethod
    def format_output(cls, json_project):
        return json.dumps(json_project, indent=2).encode("utf-8").decode("unicode_escape")
