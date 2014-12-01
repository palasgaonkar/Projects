from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import loader, Context, RequestContext
from django.http import HttpResponse

from django.utils import timezone

from django.template import loader, Context
from django.http import HttpResponse

from portal.models import BlogPost


@login_required
def skills(request):
    t = loader.get_template("blog/try-skills.html")
    return HttpResponse(t.render)


@login_required
def archive(request):
    posts = BlogPost.objects.all()
    t = loader.get_template("blog/archive.html")
    c = RequestContext(request, {'posts': posts})
    return HttpResponse(t.render(c))


# @login_required
def link(request, url):
    posts = BlogPost.objects.all()
    t = loader.get_template("blog/article.html")
    for post in posts:
        if post.id == int(url[:-1]):
            c = RequestContext(request, {'post': post})
            return HttpResponse(t.render(c))


@login_required
def edit(request, url):
    posts = BlogPost.objects.all()
    t = loader.get_template("blog/edit.html")
    for post in posts:
        if post.id == int(url[:-1]):
            c = RequestContext(request, {'post': post})
            return HttpResponse(t.render(c))


@login_required
def save(request, url):
    posts = BlogPost.objects.all()
    for post in posts:
        if post.id == int(url):
            b = BlogPost(body=request.GET.get('body'), title=request.GET.get('title'), id=post.id,
                         timestamp=timezone.now())
            b.save()
            t = loader.get_template("blog/article.html")
            c = RequestContext(request, {'post': b})
            return HttpResponse(t.render(c))


@login_required
def delete(request, url):
    posts = BlogPost.objects.all()
    for post in posts:
        if post.id == int(url):
            post.delete()
            return archive(request)


@login_required
def new(request):
    t = loader.get_template("blog/create.html")
    c = Context()
    return HttpResponse(t.render(c))


@login_required
def create(request):
    b = BlogPost(body=request.GET.get('body'), title=request.GET.get('title'), timestamp=timezone.now())
    b.save()
    return archive(request)


@login_required
def portal_main_page(request):
    """
    If users are authenticated, direct them to the main page. Otherwise, take
    them to the login page.
    """
    t = loader.get_template("blog/archive.html")
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))
