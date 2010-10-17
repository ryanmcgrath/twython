from django.conf.urls.defaults import *
from twitter.views import twitter_begin_auth, twitter_thanks, twitter_logout, twitter_timeline

urlpatterns = patterns('',
	(r'^login/?$', twitter_begin_auth),
	(r'^/logout?$', twitter_logout),
	(r'^thanks/?$', twitter_thanks), # Where they're redirect to after authorizing
	(r'^timeline/?$', twitter_timeline),
)
