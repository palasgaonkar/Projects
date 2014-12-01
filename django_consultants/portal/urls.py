from django.conf.urls.defaults import *
from portal.views import *

urlpatterns = patterns ('',
                        # Main web portal entrance.
                        # (r'^$', portal_main_page),

                        # Blog urls
                        url(r'^$', archive),
                        url(r'^skills/$', skills),
                        url(r'^article/(?P<url>.*)$', link),
                        url(r'^edit/(?P<url>.*)$', edit),
                        url(r'^new/$', new),
                        url(r'^create/$', create),
                        url(r'^save/(?P<url>.*)$', save),
                        url(r'^delete/(?P<url>.*)$', delete),

)
