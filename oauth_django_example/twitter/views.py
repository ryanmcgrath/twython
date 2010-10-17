from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from twython import Twython
from twitter.models import Profile

CONSUMER_KEY = "piKE9TwKoAhJoj7KEMlwGQ"
CONSUMER_SECRET = "RA9IzvvzoLAFGOOoOndm1Cvyh94pwPWLy4Grl4dt0o"

def twitter_logout(request):
	logout(request)
	return HttpResponseRedirect('/')

def twitter_begin_auth(request):
	# Instantiate Twython with the first leg of our trip.
	twitter = Twython(
		twitter_token = CONSUMER_KEY,
		twitter_secret = CONSUMER_SECRET
	)
	
	# Request an authorization url to send the user to...
	auth_props = twitter.get_authentication_tokens()
	
	# Then send them over there, durh.
	request.session['request_token'] = auth_props
	return HttpResponseRedirect(auth_props['auth_url'])

def twitter_thanks(request):
	# Now that we've got the magic tokens back from Twitter, we need to exchange
	# for permanent ones and store them...
	twitter = Twython(
		twitter_token = CONSUMER_KEY,
		twitter_secret = CONSUMER_SECRET,
		oauth_token = request.session['request_token']['oauth_token'],
		oauth_token_secret = request.session['request_token']['oauth_token_secret']
	)
	
	# Retrieve the tokens we want...
	authorized_tokens = twitter.get_authorized_tokens()
	
	# If they already exist, grab them, login and redirect to a page displaying stuff.
	try:
		user = User.objects.get(username = authorized_tokens['screen_name'])
	except User.DoesNotExist:
		# We mock a creation here; no email, password is just the token, etc.
		user = User.objects.create_user(authorized_tokens['screen_name'], "fjdsfn@jfndjfn.com", authorized_tokens['oauth_token_secret'])
		profile = Profile()
		profile.user = user
		profile.oauth_token = authorized_tokens['oauth_token']
		profile.oauth_secret = authorized_tokens['oauth_token_secret']
		profile.save()
	
	user = authenticate(
		username = authorized_tokens['screen_name'],
		password = authorized_tokens['oauth_token_secret']
	)
	login(request, user)
	return HttpResponseRedirect('/timeline')

def twitter_timeline(request):
	user = request.user.get_profile()
	twitter = Twython(
		twitter_token = CONSUMER_KEY,
		twitter_secret = CONSUMER_SECRET,
		oauth_token = user.oauth_token,
		oauth_token_secret = user.oauth_secret
	)
	my_tweets = twitter.getHomeTimeline()
	print my_tweets
	return render_to_response('tweets.html', {'tweets': my_tweets})
