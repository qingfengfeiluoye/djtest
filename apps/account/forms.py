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
