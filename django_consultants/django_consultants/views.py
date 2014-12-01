
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from portal.models import BlogPost
from django.template import loader, Context
from django.http import HttpResponse


def main_page(request):
    posts = BlogPost.objects.all()
    t = loader.get_template('index.html')
    c = Context({'posts': posts})
    return HttpResponse(t.render(c))


def logout_page(request):
    """
    Log users out and re-direct them to the main page.
    """
    logout(request)
    return HttpResponseRedirect('/')
