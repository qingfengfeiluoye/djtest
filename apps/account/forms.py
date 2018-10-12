from django import forms
from apps.forms_error import FormErrors


class LoginForm(forms.Form, FormErrors):
    telephone = forms.CharField(max_length="11", min_length="11",
                                error_messages={"max_length": "手机号码长度过长",
                                                "min_length": "手机号码长度过短",
                                                "required": "手机号码不能为空"})
    password = forms.CharField(max_length="25", min_length="6",
                               error_messages={"max_length": "密码长度大于25",
                                               "min_length": "密码长度小于6",
                                               "required": "密码不能为空"})
    remember = forms.BooleanField(required=False)


class SmsForm(forms.Form, FormErrors):
    telephone = forms.CharField(max_length="11", min_length="11",
                                error_messages={"max_length": "手机号码长度过长",
                                                "min_length": "手机号码长度过短",
                                                "required": "手机号码不能为空"})


class RegisterForm(forms.Form, FormErrors):
    telephone = forms.CharField(max_length="11", min_length="11",
                                error_messages={"max_length": "手机号码长度过长",
                                                "min_length": "手机号码长度过短",
                                                "required": "手机号码不能为空"})
    password = forms.CharField(max_length="25", min_length="6",
                               error_messages={"max_length": "密码长度大于25",
                                               "min_length": "密码长度小于6",
                                               "required": "密码不能为空"})
    password_repeat = forms.CharField(max_length="25", min_length="6",
                                      error_messages={"max_length": "密码长度大于25",
                                                      "min_length": "密码长度小于6",
                                                      "required": "密码不能为空"})
    username = forms.CharField(max_length="20", min_length="1",
                               error_messages={"max_length": "用户名长度过长",
                                               "min_length": "用户名长度过短",
                                               "required": "用户名不能为空"})
    sms_captcha = forms.CharField(max_length="6", min_length="6",
                                  error_messages={"max_length": "短信验证码输入错误",
                                                  "min_length": "短信验证码输入错误",
                                                  "required": "短信验证码输入错误"})
    img_captcha = forms.CharField(max_length="4", min_length="4",
                                  error_messages={"max_length": "验证码输入错误",
                                                  "min_length": "验证码输入错误",
                                                  "required": "验证码输入错误"})
