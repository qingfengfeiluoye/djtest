from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from ..news.models import NewTag, NewsPub
from untils import status_code
from untils.qiniu import qiniu
from django.http import QueryDict
from django.conf import settings
from django.http import JsonResponse
import os
from .forms import NewsForm
from django.core.paginator import Paginator
from django.http import Http404


# 非员工账号不能访问
@staff_member_required(login_url="account/login/")
def index(request):
    return render(request, "admin/index.html")


@method_decorator([csrf_exempt, staff_member_required(login_url="account/login/")], name="dispatch")
class NewTagView(View):
    # 显示所有标签
    def get(self, request):
        tags = NewTag.objects.filter(is_delete=False).all()
        # print(dir(tags.first()))
        # print(tags.first().newspub_set.all())
        return render(request, "admin/news/news_tag_manage.html", context={"tags": tags})

    # 创建标签
    def post(self, request):
        tag_name = request.POST.get("name")
        if tag_name:
            tag = NewTag.objects.filter(name=tag_name).first()
            if tag:
                return status_code.params_error(message="标签已存在，请不要重复创建")
            NewTag.objects.create(name=tag_name)
            return status_code.result(message="创建成功")
        return status_code.params_error(message="标签名不能为空")

    # 修改标签
    def put(self, request):
        tag_put = QueryDict(request.body)
        tag_name = tag_put.get("tag_name")
        tag_id = tag_put.get("tag_id")
        if tag_name and tag_id:
            tag = NewTag.objects.filter(name=tag_name).first()
            if tag:
                return status_code.params_error(message="标签已存在，请不要重复创建")
            NewTag.objects.filter(id=tag_id).update(name=tag_name)
            return status_code.result(message="修改成功")
        return status_code.params_error(message="标签不存在")

    # 删除标签
    def delete(self, request):
        tag_del = QueryDict(request.body)
        tag_id = tag_del.get("tag_id")
        if tag_id:
            tag = NewTag.objects.filter(id=tag_id)
            if tag:
                tag.update(is_delete=True)
                return status_code.result(message="删除成功")
            return status_code.params_error(message="标签不存在")
        return status_code.params_error(message="标签不存在")


@method_decorator([csrf_exempt, staff_member_required(login_url="account/login/")], name="dispatch")
class NewsPubView(View):
    def get(self, request):
        tags = NewTag.objects.filter(is_delete=False).all()
        return render(request, "admin/news/news_pub.html", context={"tags": tags})

    def post(self, request):
        form = NewsForm(request.POST)
        if form.is_valid():
            author = request.user
            title = form.cleaned_data.get("title")
            desc = form.cleaned_data.get("desc")
            tag_id = form.cleaned_data.get("tag_id")
            tag = NewTag.objects.filter(id=tag_id).first()
            img_url = form.cleaned_data.get("thumbnail_url")
            content = form.cleaned_data.get("content")
            if tag:
                NewsPub.objects.create(title=title, desc=desc, tag=tag, img_url=img_url, content=content,
                                       author=author)
                return status_code.result(message="发布成功")
            return status_code.params_error(message="标签不能为空")
        return status_code.params_error(message=form.get_error())


@csrf_exempt
def file_upload(request):
    file = request.FILES.get("upload_file")
    file_name = file.name
    file_path = os.path.join(settings.MEDIA_ROOT, file_name)
    # print(file_path)
    with open(file_path, "wb") as ff:
        for chunk in file.chunks():
            ff.write(chunk)
    #  request.build_absolute_uri 获取当前页面的绝对url
    file_url = request.build_absolute_uri(settings.MEDIA_URL + file_name)
    # print(file_url)
    return status_code.result(data={"file_url": file_url})


def up_token(request):
    token = qiniu.make_token()
    # print(token)
    return JsonResponse({"uptoken": token})


class NewsManageView(View):
    def get(self, request):
        page_num = int(request.GET.get("p", 1))
        newses = NewsPub.objects.select_related("tag", "author").defer("content", "desc").filter(is_delete=False).all()
        tags = NewTag.objects.filter(is_delete=False).all()
        # 实例指定每页几篇新闻
        paginator = Paginator(newses, settings.ONE_MANAGE_PAGE_NEWS_COUNT)
        # 获取指定页码的新闻
        try:
            page = paginator.page(page_num)
        except Exception:
            raise Http404
        page_data = self.get_page_data(paginator, page)
        context = {
            "newses": page.object_list,
            "tags": tags,
            "paginator": paginator,
            "page": page
        }
        context.update(page_data)
        return render(request, "admin/news/news_manage.html", context=context)

    @staticmethod
    def get_page_data(paginator, page, around_page=2):
        # 当前页码
        current_page = page.number
        # 总页数
        total_page = paginator.num_pages
        # 左右标识位
        left_has_more = False
        right_has_more = False
        # 获取当前页左右页码
        left_start_index = current_page - around_page
        left_end_index = current_page
        if current_page <= around_page + around_page + 1:
            left_pages = range(1, left_end_index)
        else:
            left_has_more = True
            left_pages = range(left_start_index, left_end_index)
        right_start_index = current_page + 1
        right_end_index = current_page + around_page + 1
        if current_page > total_page - around_page - around_page - 1:
            right_pages = range(right_start_index, total_page + 1)
        else:
            right_has_more = True
            right_pages = range(right_start_index, right_end_index)
        return {
            "current_page": current_page,
            "total_page": total_page,
            "left_has_more": left_has_more,
            "right_has_more": right_has_more,
            "left_pages": left_pages,
            "right_pages": right_pages
        }
