from django.db import models


class NewTag(models.Model):
    name = models.CharField(max_length=20, unique=True)
    create_time = models.DateTimeField(auto_now_add=True)
    # is_delete 删除 False为不删 True为删除
    is_delete = models.BooleanField(default=False)


class NewsPub(models.Model):
    title = models.CharField(max_length=100)
    desc = models.CharField(max_length=200)
    content = models.TextField()
    pup_time = models.DateTimeField(auto_now_add=True)
    img_url = models.URLField()
    is_delete = models.BooleanField(default=False)
    author = models.ForeignKey("account.User", on_delete=models.CASCADE)
    tag = models.ForeignKey("NewTag", on_delete=models.CASCADE)

    class Meta:
        # 定义查询出来的结果是倒序
        ordering = ["-id"]


class NewsComments(models.Model):
    content = models.CharField(max_length=10000)
    create_time = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)
    news = models.ForeignKey("NewsPub", on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey("account.User", on_delete=models.CASCADE)

    class Meta:
        # 定义查询出来的结果是倒序
        ordering = ["-id"]
