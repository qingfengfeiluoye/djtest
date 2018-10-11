from django.shortcuts import render, redirect, reverse
from django.views import View
from .forms import LoginForm
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator
from untils.captcha.make_captcha import Captcha
from io import BytesIO
from untils.mached import mached
from untils.dysms_python.demo_sms_send import send_sms


# 不验证用csrf_exempt，验证用csrf_protect
# 类使用装饰器需要用method_decorator方法
@method_decorator([csrf_exempt, ], name="dispatch")
class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "account/login.html")

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get("telephone", None)
            password = form.cleaned_data.get("password", None)
            remember = form.cleaned_data.get("remember", None)
            # print(telephone, password)
            user = authenticate(username=telephone, password=password)
            if user:
                # 保持登录状态
                login(request, user)
                if remember:
                    # 如果用户勾选记住，session有效期设置为默认值14天，单位为秒
                    request.session.set_expiry(None)
                else:
                    # 如果不勾选记住，session在关闭浏览器就过期
                    request.session.set_expiry(0)
                return JsonResponse({"code": 1, "msg": "登录成功"})
            return JsonResponse({"code": 0, "msg": "账号或密码错误"})
        msg = form.get_error()
        return JsonResponse(msg)


def logout_view(request):
    logout(request)
    return redirect(reverse("account:login"))


def make_captcha(request):
    text, img = Captcha.gene_code()
    # print(text)
    # print(img)
    # 把验证码设置到session上去
    # request.session["captcha"] = captcha
    # 把验证码存到memcached数据库
    mached.set_key("captcha", text)
    out = BytesIO()
    # 以png格式保存图片
    img.save(out, "png")
    # 游标返回起始位置
    out.seek(0)
    # 设置响应类型
    res = HttpResponse(content_type="image/png")
    # 把文件写入res
    res.write(out.read())
    return res


@method_decorator([csrf_exempt, ], name="dispatch")
class RegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "account/register.html")


def send_message(request):
    import uuid
    import random
    id1 = uuid.uuid1()
    params = "{\"code\":\"%s\"}" % random.randint(100000, 1000000)
    send_sms(id1, "13631476567", "付帅帅", "SMS_142947701", params)
    return HttpResponse("ssss")