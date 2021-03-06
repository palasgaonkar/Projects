from django.utils import timezone

from django.template import loader, Context
from django.http import HttpResponse

from blog.models import BlogPost


def skills(request):
    t = loader.get_template("try-skills.html")
    return HttpResponse(t.render)


def archive(request):
    posts = BlogPost.objects.all()
    t = loader.get_template("archive.html")
    c = Context({'posts': posts})
    return HttpResponse(t.render(c))


def link(request, url):
    posts = BlogPost.objects.all()
    t = loader.get_template("article.html")
    for post in posts:
        if post.id == int(url[:-1]):
            c = Context({'post': post})
            return HttpResponse(t.render(c))


def edit(request, url):
    posts = BlogPost.objects.all()
    t = loader.get_template("edit.html")
    for post in posts:
        if post.id == int(url[:-1]):
            c = Context({'post': post})
            return HttpResponse(t.render(c))


def save(request, url):
    posts = BlogPost.objects.all()
    for post in posts:
        if post.id == int(url):
            b = BlogPost(body=request.GET.get('body'), title=request.GET.get('title'), id=post.id,
                         timestamp=timezone.now())
            b.save()
            t = loader.get_template("article.html")
            c = Context({'post': b})
            return HttpResponse(t.render(c))


def delete(request, url):
    posts = BlogPost.objects.all()
    for post in posts:
        if post.id == int(url):
            post.delete()
            return archive(request)


def new(request):
    t = loader.get_template("create.html")
    c = Context()
    return HttpResponse(t.render(c))


def create(request):
    b = BlogPost(body=request.GET.get('body'), title=request.GET.get('title'), timestamp=timezone.now())
    b.save()
    return archive(request)
