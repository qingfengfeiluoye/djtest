class FormErrors(object):
    def get_error(self):
        if hasattr(self, "errors"):  # 判断是否有错误存在
            errors = self.errors.get_json_data()
            error_list = []
            for i in range(len(errors)):
                error_list.append(errors.popitem()[1][0]["message"])
            # if len(errors) == 2:
            #     first_error = errors.popitem()[1][0]["message"]
            #     second_error = errors.popitem()[1][0]["message"]
            #     msg = "%s,%s" % (first_error, second_error)
            #     error = {"code": 0, "msg": msg}
            #     return error
            # else:
            #     msg = errors.popitem()[1][0]["message"]
            error = {"code": 0, "msg": error_list}
            return error
        return None
