import memcache

# 建立连接
mc = memcache.Client(["127.0.0.1:11211"], debug=True)


# 设置key
def set_key(key=None, val=None, time=60000):
    if key:
        mc.set(key, val, time)
        return True
    return key


# 获取key的值
def get_key(key=None):
    if key:
        val = mc.get(key)
        return val
    return key


# 删除key
def del_key(key):
    if key:
        mc.delete(key)
        return True
    return key


set_key("12345a".lower(), "12345a".lower())
# print(get_key("iwlqam"))
