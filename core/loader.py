import csv
import io
import json
import os
import yaml


class Load:
    @classmethod
    def load_yml(self, yml_file):
        """读取yaml文件内容"""
        if not yml_file.endswith('.json'):
            with open(yml_file, "r", encoding="utf-8") as f:
                yml_content = f.read()
                loaded_json = yaml.load(yml_content, Loader=yaml.FullLoader)
            return loaded_json
        else:
            with open(yml_file, "r", encoding="utf-8") as f:
                result = f.read()
            result = json.loads(result)
            return result

    @classmethod
    def load_csv(self):
        """加载csv文件"""
        csv_file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(csv_file_path + "/data/", "login.csv")
        csv_content_list = []
        with io.open(path, encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                csv_rander = csv.DictReader(csvfile, fieldnames=row)
                for row in csv_rander:
                    csv_dict = dict(row)
                    csv_content_list.append(csv_dict)
        return csv_content_list
if __name__ == '__main__':
    r = Load().load_yml(r"C:\Users\Administrator\Desktop\hogwarts-httprunner\tests\api\get_login_1.json")
    print(type(r))
    print(r)