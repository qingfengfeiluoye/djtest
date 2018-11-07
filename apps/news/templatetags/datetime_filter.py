from django import template
from datetime import datetime
from django.utils.timezone import now

register = template.Library()


# 注册过滤器
@register.filter
def time_filter(val):
    if not isinstance(val, datetime):
        return val
    # 获取当前时间
    time_now = now()
    # 把时间戳转成秒
    s = (time_now - val).total_seconds()
    if 0 <= s < 60:
        return "刚刚"
    elif 60 <= s < 60 * 60:
        ms = int(s / 60)
        return "{}分钟前".format(ms)
    elif 60 * 60 <= s < 60 * 60 * 24:
        hour = int(s / (60 * 60))
        return "{}小时前".format(hour)
    elif 60 * 60 * 24 <= s < 60 * 60 * 24 * 2:
        return "昨天"
    elif 60 * 60 * 24 * 2 <= s < 60 * 60 * 24 * 28:
        day = int(s / (60 * 60 * 24))
        return "{}天前".format(day)
    else:
        return val.strftime('%Y/%m/%d %H:%M')
