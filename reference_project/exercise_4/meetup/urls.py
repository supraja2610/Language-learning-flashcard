from django.conf.urls import patterns, url

from meetup.views.home import home
from meetup.views.group import group_create, group_view, group_update
from meetup.views.activity import activity_create, activity_view, activity_update
from meetup.views.user import user_login, user_create, user_dashboard
from meetup.views.connect import twitter_request, twitter_access, twitter_disconnect
from meetup.views.vote import vote
from meetup.views.flickr import flickr_get_image_list

urlpatterns = patterns('',
    url(r'^home/', home, name='home'),
    url(r'^$', home, name='home'),
    url(r'^group/create/', group_create, name='group_create'),
    url(r'^group/(?P<pk>\d+)/view/', group_view, name='group_view'),
    url(r'^group/(?P<pk>\d+)/update/', group_update, name='group_update'),
    url(r'^group/(?P<group_pk>\d+)/activity/create/', activity_create,
        name='activity_create'),
    url(r'^group/(?P<group_pk>\d+)/activity/(?P<pk>\d+)/view/',
        activity_view, name='activity_view'),
    url(r'^group/(?P<group_pk>\d+)/activity/(?P<pk>\d+)/update/',
        activity_update, name='activity_update'),
    url(r'^group/(?P<group_pk>\d+)/activity/(?P<activity_pk>\d+)/vote/(?P<value>-1|0|1)/',
        vote, name='vote'),
    url(r'^user/create/', user_create, name='user_create'),
    url(r'^user/login/', user_login, name='user_login'),
    url(r'^user/logout/', 'django.contrib.auth.views.logout_then_login',
        name='user_logout'),
    url(r'^user/dashboard/', user_dashboard, name='user_dashboard'),
    url(r'^connect/twitter-request/', twitter_request, name='twitter_request'),
    url(r'^connect/twitter-access/', twitter_access, name='twitter_access'),
    url(r'^connec/twitter-disconnect/', twitter_disconnect, name='twitter_disconnect'),
    url(r'^api/flickr/(?P<query>[a-zA-Z ,.-]+)/', flickr_get_image_list, name='api_flickr')
)
