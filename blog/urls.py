from django.conf.urls.defaults import *
from django.contrib.syndication.views import Feed
from blog.views import archive, link, edit, save, create, new, delete, skills
from blog.feeds import RSSFeed

urlpatterns = patterns('',
                       url(r'^$', archive),
                       url(r'^skills/$', skills),
                       url(r'^article/(?P<url>.*)$', link),
                       url(r'^edit/(?P<url>.*)$', edit),
                       url(r'^new/$', new),
                       url(r'^create/$', create),
                       url(r'^save/(?P<url>.*)$', save),
                       url(r'^delete/(?P<url>.*)$', delete),
                       url(r'^feeds/(?P<url>.*)/$', Feed().get_feed, {'feed_dict': {'rss': RSSFeed}}),
)
