from django import forms
from apps.forms_error import FormErrors


class NewsForm(forms.Form, FormErrors):
    title = forms.CharField(max_length=100, min_length=1, error_messages={"required": "标题不能为空",
                                                                          "max_length": "标题不能超过100字",
                                                                          "min_length=": "标题不能少于1个字"
                                                                          })
    desc = forms.CharField(max_length=200, min_length=1, error_messages={"required": "标题不能为空",
                                                                         "max_length": "标题不能超过100字",
                                                                         "min_length=": "标题不能少于1个字"
                                                                         })
    tag_id = forms.IntegerField(error_messages={"required": "标题不能为空"})
    thumbnail_url = forms.URLField()
    content = forms.CharField(max_length=100000, error_messages={"required": "标题不能为空",
                                                                 "max_length": "内容不能超过100000字"})
