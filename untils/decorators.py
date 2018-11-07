from untils.status_code import un_auth_error
from functools import wraps
from django.shortcuts import redirect, reverse


def login_ajax_required(view_fun):
    @wraps(view_fun)
    def wrapper(request, *args, **kwargs):
        # 判断用户是否登录，若登录则继续
        if request.user.is_authenticated:
            return view_fun(request, *args, **kwargs)
        else:
            # 判断请求是否为ajax
            if request.is_ajax():
                return un_auth_error(message="请登录后再评论")
            else:
                # 重定向至登录页面
                return redirect(reverse("account:login"))

    return wrapper
