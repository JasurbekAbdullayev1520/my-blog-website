from datetime import datetime

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from django.shortcuts import render

def home(request):
    return render(request, 'home.html')


class HomeView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "home.html", {"posts": posts[-2:]})


class BlogsView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        query_params = request.GET
        if query_params.get("search"):
            search = query_params["search"]

            result = []
            for post in posts:
                if search.lower() in post["title"].lower():
                    result.append(post)

            return render(request, "blog.html", {"posts": result, "search": search})

        return render(request, "blog.html", {"posts": posts[::-1]})


class BlogDetailView(View):
    def get(self, request: HttpRequest, slug: str) -> HttpResponse:
        for post in posts:
            if post["slug"] == slug:
                post["views"] += 1
                return render(request, "blog_detail.html", {"post": post})
        return render(
            request, "blog.html", {"posts": posts, "error": f"{slug} is not found."}
        )


class BlogCreateView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "blog_create.html")

    def post(self, request: HttpRequest) -> HttpResponse:
        post_data = request.POST

        posts.append(
            {
                "id": 4,
                "title": post_data.get("title"),
                "slug": post_data.get("slug"),
                "reading_minute": post_data.get("reading_minute"),
                "content": post_data.get("content"),
                "tg_link": post_data.get("tg_link"),
                "views": 0,
            }
        )

        return redirect(reverse("blogs"))


class BlogDeleteView(View):
    def get(self, request: HttpRequest, id=None) -> HttpResponse:
        return render(request, "blog_delete.html", {"blogs": posts})

    def post(self, request: HttpRequest, id: int) -> HttpResponse:
        global posts
        posts = [post for post in posts if post["id"] != id]
        return redirect("blog_delete_list")


class BlogUpdateView(View):
    def get(self, request: HttpRequest, id: int) -> HttpResponse:
        post = next((p for p in posts if p["id"] == id), None)
        if not post:
            return redirect("blogs")
        return render(request, "blog_update.html", {"post": post})

    def post(self, request: HttpRequest, id: int) -> HttpResponse:
        post_data = request.POST

        for post in posts:
            if post["id"] == id:
                post["title"] = post_data.get("title")
                post["slug"] = post_data.get("slug")
                post["reading_minute"] = post_data.get("reading_minute")
                post["content"] = post_data.get("content")
                post["tg_link"] = post_data.get("tg_link")
                break

        return redirect(reverse("blog_detail", kwargs={"slug": post_data.get("slug")}))

# Create your views here.
