from django.views.generic import View
from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin


# トップページ
class IndexView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by("-id")
        return render(
            request,
            "app/index.html",
            {
                "post_data": post_data,
            },
        )


# get関数はviewはコールされたら最初に呼ばれる関数
# post modelからデータを取得
# order_byで並び替え可能　-idを指定すると降順になる


class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs["pk"])
        return render(request, "app/post_detail.html", {"post_data": post_data})


# 詳細画面用


class CreatePostView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)

        return render(request, "app/post_form.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)

        if form.is_valid():
            post_data = Post()
            post_data.author = request.user
            post_data.title = form.cleaned_data["title"]
            post_data.content = form.cleaned_data["content"]
            post_data.save()
            return redirect("post_detail", post_data.id)

        return render(request, "app/post_form.html", {"form": form})


# 投稿編集
class PostEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs["pk"])
        form = PostForm(
            request.POST or None,
            initial={
                "title": post_data.title,
                "content": post_data.content,
            },
        )
        # ホームをテンプレートへかえす
        return render(request, "app/post_form.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)

        if form.is_valid():
            post_data = Post.objects.get(id=self.kwargs["pk"])
            post_data.title = form.cleaned_data["title"]
            post_data.content = form.cleaned_data["content"]
            post_data.save()
            return redirect("post_detail", self.kwargs["pk"])

        return render(request, "app/post_form.html", {"form": form})


class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs["pk"])
        return render(request, "app/post_delete.html", {"post_data": post_data})

    def post(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs["pk"])
        post_data.delete()
        return redirect("index")
