from django import forms
from ..forms_error import FormErrors


class CommentsForm(forms.Form, FormErrors):
    news_id = forms.CharField(error_messages={"required": "新闻id不能为空"})
    content = forms.CharField(error_messages={"required": "评论不能为空"})
