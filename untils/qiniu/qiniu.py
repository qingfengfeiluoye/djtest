from qiniu import Auth, put_file, etag
import qiniu.config

# 需要填写你的 Access Key 和 Secret Key
access_key = 'cdFPS53dom8Raj4u6nI8QHmXpKsAHyhN15r1vBy1'
secret_key = '-psPvDbRUtfQCa02crmiJPfkcJWM_aDIDXHK55Lc'
# 构建鉴权对象
q = Auth(access_key, secret_key)
# 要上传的空间
bucket_name = 'fubbs'
# 上传到七牛后保存的文件名
key = 'my-python-logo.png'


# 生成上传 Token，可以指定过期时间等
def make_token():
    token = q.upload_token(bucket_name, key, 3600)
    return token
# 要上传文件的本地路径
# localfile = './sync/bbb.jpg'
# ret, info = put_file(token, key, localfile)
# print(info)
# assert ret['key'] == key
# assert ret['hash'] == etag(localfile)
