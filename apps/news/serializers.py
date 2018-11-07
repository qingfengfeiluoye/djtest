from rest_framework import serializers
from .models import NewsComments, NewsPub, NewTag
from apps.account.serializers import UserSerializer


class CommentSerializers(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = NewsComments
        fields = ("id", "content", "create_time", "author")


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = NewTag
        fields = ("name",)


class NewsSerializers(serializers.ModelSerializer):
    author = UserSerializer()
    tag = TagSerializers()

    class Meta:
        model = NewsPub
        fields = ("id", "title", "desc", "pup_time", "img_url", "author", "tag")
