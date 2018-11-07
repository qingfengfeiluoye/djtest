from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from .models import NewsPub, NewTag, NewsComments
from django.http import Http404
from .serializers import CommentSerializers, NewsSerializers
from untils import status_code
from .forms import CommentsForm
from untils.decorators import login_ajax_required
from django.conf import settings


@method_decorator([csrf_exempt, ], name="dispatch")
class IndexView(View):
    def get(self, request):
        news = NewsPub.objects.select_related("tag", "author").filter(is_delete=False).defer("content").all()[
               0:settings.ONE_PAGE_NEWS_COUNT]
        tags = NewTag.objects.filter(is_delete=False).all()
        context = {"news": news, "tags": tags}
        return render(request, "news/index.html", context=context)


# 新闻分页加载 news/list/
def news_list(request):
    page = int(request.GET.get("page", 1))
    tag_id = int(request.GET.get("tag_id", 0))
    # print(tag_id, page)
    start_index = settings.ONE_PAGE_NEWS_COUNT * (page - 1)
    end_index = start_index + settings.ONE_PAGE_NEWS_COUNT
    if tag_id:
        newses = NewsPub.objects.select_related("tag", "author").filter(is_delete=False, tag=tag_id).defer(
            "content").all()[start_index:end_index]
    else:
        newses = NewsPub.objects.select_related("tag", "author").filter(is_delete=False).defer("content").all()[
                 start_index:end_index]
    serializer = NewsSerializers(newses, many=True)
    return status_code.result(data={"newses": serializer.data})


def news_details(request, news_id):
    try:
        news = NewsPub.objects.get(id=news_id)
        return render(request, "news/news_detail.html", context={"news": news})
    # news_id 不存在就返回404
    except NewsPub.DoesNotExist:
        raise Http404


# 新闻被评论时调用
@method_decorator([csrf_exempt, login_ajax_required], name="dispatch")
class NewsAddComments(View):
    def get(self, request):
        pass

    def post(self, request):
        form = CommentsForm(request.POST)
        if form.is_valid():
            news_id = form.cleaned_data.get("news_id")
            content = form.cleaned_data.get("content")
            news = NewsPub.objects.filter(id=news_id).first()
            if news:
                # 保存评论至数据库
                comments = NewsComments.objects.create(news=news, content=content, author=request.user)
                # 把新增评论序列化
                serializers = CommentSerializers(comments)
                return status_code.result(data=serializers.data)
            return status_code.params_error(message="新闻不存在")
        return status_code.params_error(message=form.get_error())


# 打开某条新闻时调用，查出改新闻的所有评论
def news_comments(request):
    news_id = int(request.GET.get("news_id"))
    news = NewsPub.objects.filter(id=news_id, is_delete=False).first()
    if news:
        # 反向查询获得指定新闻的所有评论
        comments_all = news.comments.all()
        # 序列化多条数据时需要参数many=True
        serializers = CommentSerializers(comments_all, many=True)
        return status_code.result(data=serializers.data)
    return status_code.params_error(message="新闻不存在")


class SearchView(View):
    def get(self, request):
        return render(request, "news/search.html")
