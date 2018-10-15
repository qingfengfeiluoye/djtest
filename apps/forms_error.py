class FormErrors(object):
    def get_error(self):
        if hasattr(self, "errors"):  # 判断是否有错误存在
            error_json = self.errors.get_json_data()  # 获取json格式数据
            error_tuple = error_json.popitem()
            error_list = error_tuple[1]
            error_dict = error_list[0]
            message = error_dict["message"]
            return message
        return None
