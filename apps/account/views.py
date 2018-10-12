from django.shortcuts import render, redirect, reverse
from django.views import View
from .forms import LoginForm, SmsForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator
from untils.captcha.make_captcha import Captcha
from io import BytesIO
from untils.mached import mached
from untils.dysms_python.demo_sms_send import send_sms
from .models import User


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
    # request.session["img_captcha"] = text
    # 把验证码存到memcached数据库
    mached.set_key("img_captcha", text)
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

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get("telephone")
            password = form.cleaned_data.get("password")
            password_repeat = form.cleaned_data.get("password_repeat")
            username = form.cleaned_data.get("username")
            sms_captcha = form.cleaned_data.get("sms_captcha")
            img_captcha = form.cleaned_data.get("img_captcha")
            user = User.objects.filter(telephone=telephone).first()
            mc_sms_captcha = mached.get_key("sms_captcha")
            mc_img_captcha = mached.get_key("img_captcha")
            # print(int(mc_sms_captcha), type(sms_captcha))
            # print(mc_img_captcha, img_captcha)
            if user:
                return JsonResponse({"code": 0, "msg": "该手机号码已注册，请登录"})
            elif password != password_repeat:
                return JsonResponse({"code": 0, "msg": "两次密码输入不一致，请重新输入"})
            else:
                if sms_captcha.isdigit():
                    if int(sms_captcha) == int(mc_sms_captcha) and img_captcha == mc_img_captcha:
                        user = User.objects._create_user(telephone, username, password)
                        login(request, user)
                        request.session.set_expiry(0)
                        return JsonResponse({"code": 1, "msg": "注册成功"})
                else:
                    return JsonResponse({"code": 0, "msg": "验证码输入错误，请重新输入"})
                return JsonResponse({"code": 0, "msg": "手机验证码输入错误，请重新输入"})
        return JsonResponse({"code": 0, "msg": "验证码输入错误，请重新输入"})


@method_decorator([csrf_exempt, ], name="dispatch")
class SendMessageView(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        form = SmsForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get("telephone")
            print(telephone)
            import uuid
            import random
            id1 = uuid.uuid1()
            captcha_num = random.randint(100000, 1000000)
            mached.set_key("sms_captcha", captcha_num)
            params = "{\"code\":\"%s\"}" % captcha_num
            send_sms(id1, telephone, "付帅帅", "SMS_142947701", params)
            return JsonResponse({"code": 1, "msg": "验证码发送成功"})
        else:
            msg = form.get_error()
            return JsonResponse(msg)
