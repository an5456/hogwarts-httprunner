import yaml


def load_yml(yml_file):
    """读取yaml文件内容"""
    with open(yml_file, "r", encoding="utf-8") as f:
        yml_content = f.read()
        loaded_json = yaml.load(yml_content, Loader=yaml.FullLoader)
    return loaded_json

