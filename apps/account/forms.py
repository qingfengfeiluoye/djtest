from django import forms
from apps.forms_error import FormErrors
from untils.mached import mached


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

    def check_captcha(self):
        sms_captcha = self.cleaned_data.get("sms_captcha")
        img_captcha = self.cleaned_data.get("img_captcha")
        mc_sms_captcha = mached.get_key(sms_captcha.lower())
        mc_img_captcha = mached.get_key(img_captcha.lower())
        password = self.cleaned_data.get("password")
        password_repeat = self.cleaned_data.get("password_repeat")
        if password != password_repeat:
            return self.add_error("password", "两次输入密码不一致，请重新输入")
        if not mc_img_captcha and mc_img_captcha != img_captcha:
            return self.add_error("img_captcha", "图形验证码输入错误，请重新输入")
        if not mc_sms_captcha and mc_sms_captcha != sms_captcha:
            return self.add_error("sms_captcha", "短信验证码输入错误，请重新输入")
        return True
