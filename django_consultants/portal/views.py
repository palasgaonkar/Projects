from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.template import loader, Context, RequestContext
from django.http import HttpResponse

@login_required
def portal_main_page(request):
    """
    If users are authenticated, direct them to the main page. Otherwise, take
    them to the login page.
    """
    t = loader.get_template("portal/index.html")
    c = RequestContext(request, {})
    return HttpResponse(t.render(c))
