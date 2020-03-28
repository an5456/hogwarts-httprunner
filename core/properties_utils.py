class Properties:
    def __init__(self, filename):
        self.properties_filename = filename
        self.properties = {}

    def get_properties(self) -> dict:
        with open(self.properties_filename, "r", encoding="UTF-8") as pro_file:
            for line in pro_file.readlines():
                # 去掉两端的空格和\n换行符
                line = line.strip().replace("\n", " ")
                # 如果发现#符合，代表这一行或者后面是注释内容
                if line.find("#") != -1:
                    line = line[0:line.find("#")]
                # 如果包含了等号，我们就要进行字典类型的转换处理
                if line.find("=") > 0:
                    # 用=切分，形成新的字符串类型的list
                    strs = line.split("=")
                    # 获取字典
                    self.__get_dict(strs[0].strip(), self.properties, strs[1].strip())
        return self.properties

    def __get_dict(self, key_name, result_dict, value):

        # 检查key总是否包含"."，包含的话我们就切分，不包含的话就直接设置值就可以了
        if key_name.find(".") > 0:
            k = key_name.split(".")[0]  # scm.csjmro.com = 192.168.135
            result_dict.setdefault(k, {})  # 'scm': {'csjmro': {'com': '192.168.135'}}
            return self.__get_dict(key_name[len(k) + 1:], result_dict[k], value)
        else:
            result_dict[key_name] = value


if __name__ == '__main__':
    print(Properties('log.properties').get_properties())