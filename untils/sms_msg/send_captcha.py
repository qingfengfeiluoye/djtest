from untils.dysms_python.demo_sms_send import send_sms
from untils.mached import mached

captcha_str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789"


def send_captcha(telephone):
    import uuid
    import random
    id1 = uuid.uuid1()
    captcha_num = "".join(random.sample(captcha_str, 6))
    mached.set_key(captcha_num.lower(), captcha_num.lower())
    params = "{\"code\":\"%s\"}" % captcha_num
    res = send_sms(id1, telephone, "付帅帅", "SMS_142947701", params)
    return res
