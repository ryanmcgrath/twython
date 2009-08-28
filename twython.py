#!/usr/bin/python

"""
	Twython is an up-to-date library for Python that wraps the Twitter API.
	Other Python Twitter libraries seem to have fallen a bit behind, and
	Twitter's API has evolved a bit. Here's hoping this helps.

	TODO: OAuth, Streaming API?

	Questions, comments? ryan@venodesigns.net
"""

import httplib, urllib, urllib2, mimetypes, mimetools

from urlparse import urlparse
from urllib2 import HTTPError

__author__ = "Ryan McGrath <ryan@venodesigns.net>"
__version__ = "0.8"

"""Twython - Easy Twitter utilities in Python"""

try:
	import simplejson
except ImportError:
	try:
		import json as simplejson
	except:
		raise Exception("Twython requires the simplejson library (or Python 2.6) to work. http://www.undefined.org/python/")

try:
	import oauth
except ImportError:
	pass

class TwythonError(Exception):
	def __init__(self, msg, error_code=None):
		self.msg = msg
		if error_code == 400:
			raise APILimit(msg)
	def __str__(self):
		return repr(self.msg)

class APILimit(TwythonError):
	def __init__(self, msg):
		self.msg = msg
	def __str__(self):
		return repr(self.msg)

class AuthError(TwythonError):
	def __init__(self, msg):
		self.msg = msg
	def __str__(self):
		return repr(self.msg)

class setup:
	def __init__(self, authtype = "OAuth", username = None, password = None, consumer_secret = None, consumer_key = None, headers = None):
		"""setup(authtype = "OAuth", username = None, password = None, consumer_secret = None, consumer_key = None, headers = None)

			Instantiates an instance of Twython. Takes optional parameters for authentication and such (see below).

			Parameters:
				authtype - "OAuth"/"Basic"
				username - Your twitter username
				password - Password for your twitter account.
				consumer_secret - Consumer secret in case you specified for OAuth as authtype.
				consumer_key - Consumer key in case you specified for OAuth as authtype.
				headers - User agent header.
		"""
		self.authtype = authtype
		self.authenticated = False
		self.username = username
		# OAuth specific variables below
		self.request_token_url = 'https://twitter.com/oauth/request_token'
		self.access_token_url = 'https://twitter.com/oauth/access_token'
		self.authorization_url = 'http://twitter.com/oauth/authorize'
		self.signin_url = 'http://twitter.com/oauth/authenticate'
		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
		self.request_token = None
		self.access_token = None
		# Check and set up authentication
		if self.username is not None and password is not None:
			if self.authtype == "Basic":
				# Basic authentication ritual
				self.auth_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
				self.auth_manager.add_password(None, "http://twitter.com", self.username, password)
				self.handler = urllib2.HTTPBasicAuthHandler(self.auth_manager)
				self.opener = urllib2.build_opener(self.handler)
				if headers is not None:
					self.opener.addheaders = [('User-agent', headers)]
				try:
					simplejson.load(self.opener.open("http://twitter.com/account/verify_credentials.json"))
					self.authenticated = True
				except HTTPError, e:
					raise TwythonError("Authentication failed with your provided credentials. Try again? (%s failure)" % `e.code`, e.code)
			else:
				self.signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()
				# Awesome OAuth authentication ritual
				if consumer_secret is not None and consumer_key is not None:
					#req = oauth.OAuthRequest.from_consumer_and_token
					#req.sign_request(self.signature_method, self.consumer_key, self.token)
					#self.opener = urllib2.build_opener()
					pass
				else:
					raise TwythonError("Woah there, buddy. We've defaulted to OAuth authentication, but you didn't provide API keys. Try again.")

	def getRequestToken(self):
		response = self.oauth_request(self.request_token_url)
		token = self.parseOAuthResponse(response)
		self.request_token = oauth.OAuthConsumer(token['oauth_token'],token['oauth_token_secret'])
		return self.request_token

	def parseOAuthResponse(self, response_string):
		# Partial credit goes to Harper Reed for this gem.
		lol = {}
		for param in response_string.split("&"):
			pair = param.split("=")
			if(len(pair) != 2):
				break
			lol[pair[0]] = pair[1]
		return lol

	# URL Shortening function huzzah
	def shortenURL(self, url_to_shorten, shortener = "http://is.gd/api.php", query = "longurl"):
		"""shortenURL(url_to_shorten, shortener = "http://is.gd/api.php", query = "longurl")

			Shortens url specified by url_to_shorten.

			Parameters:
				url_to_shorten - URL to shorten.
				shortener - In case you want to use url shorterning service other that is.gd.
		"""
		try:
			return urllib2.urlopen(shortener + "?" + urllib.urlencode({query: self.unicode2utf8(url_to_shorten)})).read()
		except HTTPError, e:
			raise TwythonError("shortenURL() failed with a %s error code." % `e.code`)

	def constructApiURL(self, base_url, params):
		return base_url + "?" + "&".join(["%s=%s" %(key, value) for (key, value) in params.iteritems()])

	def getRateLimitStatus(self, rate_for = "requestingIP"):
		"""getRateLimitStatus()

			Returns the remaining number of API requests available to the requesting user before the
			API limit is reached for the current hour. Calls to rate_limit_status do not count against
			the rate limit.  If authentication credentials are provided, the rate limit status for the
			authenticating user is returned.  Otherwise, the rate limit status for the requesting
			IP address is returned.
		"""
		try:
			if rate_for == "requestingIP":
				return simplejson.load(urllib2.urlopen("http://twitter.com/account/rate_limit_status.json"))
			else:
				if self.authenticated is True:
					return simplejson.load(self.opener.open("http://twitter.com/account/rate_limit_status.json"))
				else:
					raise TwythonError("You need to be authenticated to check a rate limit status on an account.")
		except HTTPError, e:
			raise TwythonError("It seems that there's something wrong. Twitter gave you a %s error code; are you doing something you shouldn't be?" % `e.code`, e.code)

	def getPublicTimeline(self):
		"""getPublicTimeline()

			Returns the 20 most recent statuses from non-protected users who have set a custom user icon.
			The public timeline is cached for 60 seconds, so requesting it more often than that is a waste of resources.
		"""
		try:
			return simplejson.load(urllib2.urlopen("http://twitter.com/statuses/public_timeline.json"))
		except HTTPError, e:
			raise TwythonError("getPublicTimeline() failed with a %s error code." % `e.code`)

	def getHomeTimeline(self, **kwargs):
		"""getHomeTimeline(**kwargs)

			Returns the 20 most recent statuses, including retweets, posted by the authenticating user
			and that user's friends. This is the equivalent of /timeline/home on the Web.

			Usage note: This home_timeline is identical to statuses/friends_timeline, except it also
			contains retweets, which statuses/friends_timeline does not (for backwards compatibility
			reasons). In a future version of the API, statuses/friends_timeline will go away and
			be replaced by home_timeline.

			Parameters:
				since_id - Optional.  Returns only statuses with an ID greater than (that is, more recent than) the specified ID.
				max_id - Optional.  Returns only statuses with an ID less than (that is, older than) or equal to the specified ID. 
				count - Optional.  Specifies the number of statuses to retrieve. May not be greater than 200.  
				page - Optional. Specifies the page of results to retrieve. Note: there are pagination limits.
		"""
		if self.authenticated is True:
			try:
				homeTimelineURL = self.constructApiURL("http://twitter.com/statuses/home_timeline.json", kwargs)
				return simplejson.load(self.opener.open(homeTimelineURL))
			except HTTPError, e:
				raise TwythonError("getHomeTimeline() failed with a %s error code. (This is an upcoming feature in the Twitter API, and may not be implemented yet)" % `e.code`)
		else:
			raise AuthError("getHomeTimeline() requires you to be authenticated.")

	def getFriendsTimeline(self, **kwargs):
		"""getFriendsTimeline(**kwargs)

			Returns the 20 most recent statuses posted by the authenticating user, as well as that users friends. 
			This is the equivalent of /timeline/home on the Web.

			Parameters:
				since_id - Optional.  Returns only statuses with an ID greater than (that is, more recent than) the specified ID.
				max_id - Optional.  Returns only statuses with an ID less than (that is, older than) or equal to the specified ID. 
				count - Optional.  Specifies the number of statuses to retrieve. May not be greater than 200.  
				page - Optional. Specifies the page of results to retrieve. Note: there are pagination limits.
		"""
		if self.authenticated is True:
			try:
				friendsTimelineURL = self.constructApiURL("http://twitter.com/statuses/friends_timeline.json", kwargs)
				return simplejson.load(self.opener.open(friendsTimelineURL))
			except HTTPError, e:
				raise TwythonError("getFriendsTimeline() failed with a %s error code." % `e.code`)
		else:
			raise AuthError("getFriendsTimeline() requires you to be authenticated.")

	def getUserTimeline(self, id = None, **kwargs): 
		"""getUserTimeline(id = None, **kwargs)

			Returns the 20 most recent statuses posted from the authenticating user. It's also
			possible to request another user's timeline via the id parameter. This is the
			equivalent of the Web /<user> page for your own user, or the profile page for a third party.

			Parameters:
				id - Optional. Specifies the ID or screen name of the user for whom to return the user_timeline.
				user_id - Optional. Specfies the ID of the user for whom to return the user_timeline. Helpful for disambiguating.
				screen_name - Optional. Specfies the screen name of the user for whom to return the user_timeline. (Helpful for disambiguating when a valid screen name is also a user ID)
				since_id -  Optional.  Returns only statuses with an ID greater than (that is, more recent than) the specified ID.
				max_id - Returns only statuses with an ID less than (that is, older than) or equal to the specified ID.
				count - Optional.  Specifies the number of statuses to retrieve. May not be greater than 200.
				page - Optional. Specifies the page of results to retrieve. Note: there are pagination limits. 
		"""
		if id is not None and kwargs.has_key("user_id") is False and kwargs.has_key("screen_name") is False:
			userTimelineURL = self.constructApiURL("http://twitter.com/statuses/user_timeline/%s.json" % `id`, kwargs)
		elif id is None and kwargs.has_key("user_id") is False and kwargs.has_key("screen_name") is False and self.authenticated is True:
			userTimelineURL = self.constructApiURL("http://twitter.com/statuses/user_timeline/%s.json" % self.username, kwargs)
		else:
			userTimelineURL = self.constructApiURL("http://twitter.com/statuses/user_timeline.json", kwargs)
		try:
			# We do our custom opener if we're authenticated, as it helps avoid cases where it's a protected user
			if self.authenticated is True:
				return simplejson.load(self.opener.open(userTimelineURL))
			else:
				return simplejson.load(urllib2.urlopen(userTimelineURL))
		except HTTPError, e:
			raise TwythonError("Failed with a %s error code. Does this user hide/protect their updates? If so, you'll need to authenticate and be their friend to get their timeline."
				% `e.code`, e.code)

	def getUserMentions(self, **kwargs):
		"""getUserMentions(**kwargs)

			Returns the 20 most recent mentions (status containing @username) for the authenticating user.

			Parameters:
				since_id - Optional.  Returns only statuses with an ID greater than (that is, more recent than) the specified ID.
				max_id - Optional.  Returns only statuses with an ID less than (that is, older than) or equal to the specified ID. 
				count - Optional.  Specifies the number of statuses to retrieve. May not be greater than 200.  
				page - Optional. Specifies the page of results to retrieve. Note: there are pagination limits.
		"""
		if self.authenticated is True:
			try:
				mentionsFeedURL = self.constructApiURL("http://twitter.com/statuses/mentions.json", kwargs)
				return simplejson.load(self.opener.open(mentionsFeedURL))
			except HTTPError, e:
				raise TwythonError("getUserMentions() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("getUserMentions() requires you to be authenticated.")

	def reTweet(self, id):
		"""reTweet(id)

			Retweets a tweet. Requires the id parameter of the tweet you are retweeting.

			Parameters:
				id - Required. The numerical ID of the tweet you are retweeting.
		"""
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/statuses/retweet/%s.json", "POST" % id))
			except HTTPError, e:
				raise TwythonError("reTweet() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("reTweet() requires you to be authenticated.")

	def retweetedOfMe(self, **kwargs):
		"""retweetedOfMe(**kwargs)

			Returns the 20 most recent tweets of the authenticated user that have been retweeted by others.

			Parameters:
				since_id - Optional.  Returns only statuses with an ID greater than (that is, more recent than) the specified ID.
				max_id - Optional.  Returns only statuses with an ID less than (that is, older than) or equal to the specified ID. 
				count - Optional.  Specifies the number of statuses to retrieve. May not be greater than 200.  
				page - Optional. Specifies the page of results to retrieve. Note: there are pagination limits.
		"""
		if self.authenticated is True:
			try:
				retweetURL = self.constructApiURL("http://twitter.com/statuses/retweets_of_me.json", kwargs)
				return simplejson.load(self.opener.open(retweetURL))
			except HTTPError, e:
				raise TwythonError("retweetedOfMe() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("retweetedOfMe() requires you to be authenticated.")

	def retweetedByMe(self, **kwargs):
		"""retweetedByMe(**kwargs)

			Returns the 20 most recent retweets posted by the authenticating user.

			Parameters:
				since_id - Optional.  Returns only statuses with an ID greater than (that is, more recent than) the specified ID.
				max_id - Optional.  Returns only statuses with an ID less than (that is, older than) or equal to the specified ID. 
				count - Optional.  Specifies the number of statuses to retrieve. May not be greater than 200.  
				page - Optional. Specifies the page of results to retrieve. Note: there are pagination limits.
		"""
		if self.authenticated is True:
			try:
				retweetURL = self.constructApiURL("http://twitter.com/statuses/retweeted_by_me.json", kwargs)
				return simplejson.load(self.opener.open(retweetURL))
			except HTTPError, e:
				raise TwythonError("retweetedByMe() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("retweetedByMe() requires you to be authenticated.")

	def retweetedToMe(self, **kwargs):
		"""retweetedToMe(**kwargs)

			Returns the 20 most recent retweets posted by the authenticating user's friends.

			Parameters:
				since_id - Optional.  Returns only statuses with an ID greater than (that is, more recent than) the specified ID.
				max_id - Optional.  Returns only statuses with an ID less than (that is, older than) or equal to the specified ID. 
				count - Optional.  Specifies the number of statuses to retrieve. May not be greater than 200.  
				page - Optional. Specifies the page of results to retrieve. Note: there are pagination limits.
		"""
		if self.authenticated is True:
			try:
				retweetURL = self.constructApiURL("http://twitter.com/statuses/retweeted_to_me.json", kwargs)
				return simplejson.load(self.opener.open(retweetURL))
			except HTTPError, e:
				raise TwythonError("retweetedToMe() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("retweetedToMe() requires you to be authenticated.")

	def showUser(self, id = None, user_id = None, screen_name = None):
		"""showUser(id = None, user_id = None, screen_name = None)

			Returns extended information of a given user.  The author's most recent status will be returned inline.

			Parameters:
				** Note: One of the following must always be specified.
				id - The ID or screen name of a user.
				user_id - Specfies the ID of the user to return. Helpful for disambiguating when a valid user ID is also a valid screen name.
				screen_name - Specfies the screen name of the user to return. Helpful for disambiguating when a valid screen name is also a user ID.

			Usage Notes:
			Requests for protected users without credentials from 
				1) the user requested or
				2) a user that is following the protected user will omit the nested status element.

			...will result in only publicly available data being returned.
		"""
		if self.authenticated is True:
			apiURL = ""
			if id is not None:
				apiURL = "http://twitter.com/users/show/%s.json" % id
			if user_id is not None:
				apiURL = "http://twitter.com/users/show.json?user_id=%s" % `user_id`
			if screen_name is not None:
				apiURL = "http://twitter.com/users/show.json?screen_name=%s" % screen_name
			try:
				return simplejson.load(self.opener.open(apiURL))
			except HTTPError, e:
				raise TwythonError("showUser() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("showUser() requires you to be authenticated.")

	def getFriendsStatus(self, id = None, user_id = None, screen_name = None, page = "1"):
		"""getFriendsStatus(id = None, user_id = None, screen_name = None, page = "1")

			Returns a user's friends, each with current status inline. They are ordered by the order in which they were added as friends, 100 at a time. 
			(Please note that the result set isn't guaranteed to be 100 every time, as suspended users will be filtered out.) Use the page option to access 
			older friends. With no user specified, the request defaults to the authenticated users friends. 
			
			It's also possible to request another user's friends list via the id, screen_name or user_id parameter.

			Parameters:
				** Note: One of the following is required. (id, user_id, or screen_name)
				id - Optional. The ID or screen name of the user for whom to request a list of friends. 
				user_id - Optional. Specfies the ID of the user for whom to return the list of friends. Helpful for disambiguating when a valid user ID is also a valid screen name.
				screen_name - Optional. Specfies the screen name of the user for whom to return the list of friends. Helpful for disambiguating when a valid screen name is also a user ID.
				page - Optional. Specifies the page of friends to receive.
		"""
		if self.authenticated is True:
			apiURL = ""
			if id is not None:
				apiURL = "http://twitter.com/statuses/friends/%s.json" % id
			if user_id is not None:
				apiURL = "http://twitter.com/statuses/friends.json?user_id=%s" % `user_id`
			if screen_name is not None:
				apiURL = "http://twitter.com/statuses/friends.json?screen_name=%s" % screen_name
			try:
				return simplejson.load(self.opener.open(apiURL + "&page=%s" % `page`))
			except HTTPError, e:
				raise TwythonError("getFriendsStatus() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("getFriendsStatus() requires you to be authenticated.")

	def getFollowersStatus(self, id = None, user_id = None, screen_name = None, page = "1"):
		"""getFollowersStatus(id = None, user_id = None, screen_name = None, page = "1")

			Returns the authenticating user's followers, each with current status inline.
			They are ordered by the order in which they joined Twitter, 100 at a time.
			(Note that the result set isn't guaranteed to be 100 every time, as suspended users will be filtered out.) 
			
			Use the page option to access earlier followers.

			Parameters:
				** Note: One of the following is required. (id, user_id, screen_name)
				id - Optional. The ID or screen name of the user for whom to request a list of followers. 
				user_id - Optional. Specfies the ID of the user for whom to return the list of followers. Helpful for disambiguating when a valid user ID is also a valid screen name.
				screen_name - Optional. Specfies the screen name of the user for whom to return the list of followers. Helpful for disambiguating when a valid screen name is also a user ID.
				page - Optional. Specifies the page to retrieve. 
		"""
		if self.authenticated is True:
			apiURL = ""
			if id is not None:
				apiURL = "http://twitter.com/statuses/followers/%s.json" % id
			if user_id is not None:
				apiURL = "http://twitter.com/statuses/followers.json?user_id=%s" % `user_id`
			if screen_name is not None:
				apiURL = "http://twitter.com/statuses/followers.json?screen_name=%s" % screen_name
			try:
				return simplejson.load(self.opener.open(apiURL + "&page=%s" % `page`))
			except HTTPError, e:
				raise TwythonError("getFollowersStatus() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("getFollowersStatus() requires you to be authenticated.")


	def showStatus(self, id):
		"""showStatus(id)

			Returns a single status, specified by the id parameter below.
			The status's author will be returned inline.

			Parameters:
				id - Required. The numerical ID of the status to retrieve.
		"""
		try:
			if self.authenticated is True:
				return simplejson.load(self.opener.open("http://twitter.com/statuses/show/%s.json" % id))
			else:
				return simplejson.load(urllib2.urlopen("http://twitter.com/statuses/show/%s.json" % id))
		except HTTPError, e:
			raise TwythonError("Failed with a %s error code. Does this user hide/protect their updates? You'll need to authenticate and be friends to get their timeline." 
				% `e.code`, e.code)

	def updateStatus(self, status, in_reply_to_status_id = None):
		"""updateStatus(status, in_reply_to_status_id = None)

			Updates the authenticating user's status.  Requires the status parameter specified below.
			A status update with text identical to the authenticating users current status will be ignored to prevent duplicates.

			Parameters:
				status - Required. The text of your status update. URL encode as necessary. Statuses over 140 characters will be forceably truncated.
				in_reply_to_status_id - Optional. The ID of an existing status that the update is in reply to.

				** Note: in_reply_to_status_id will be ignored unless the author of the tweet this parameter references
				is mentioned within the status text. Therefore, you must include @username, where username is 
				the author of the referenced tweet, within the update.
		"""
		if len(list(status)) > 140:
			raise TwythonError("This status message is over 140 characters. Trim it down!")
		try:
			return simplejson.load(self.opener.open("http://twitter.com/statuses/update.json?", urllib.urlencode({"status": self.unicode2utf8(status), "in_reply_to_status_id": in_reply_to_status_id})))
		except HTTPError, e:
			raise TwythonError("updateStatus() failed with a %s error code." % `e.code`, e.code)

	def destroyStatus(self, id):
		"""destroyStatus(id)

			Destroys the status specified by the required ID parameter. 
			The authenticating user must be the author of the specified status.

			Parameters:
				id - Required. The ID of the status to destroy.
		"""
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/status/destroy/%s.json", "POST" % id))
			except HTTPError, e:
				raise TwythonError("destroyStatus() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("destroyStatus() requires you to be authenticated.")

	def endSession(self):
		"""endSession()

			Ends the session of the authenticating user, returning a null cookie. 
			Use this method to sign users out of client-facing applications (widgets, etc).
		"""
		if self.authenticated is True:
			try:
				self.opener.open("http://twitter.com/account/end_session.json", "")
				self.authenticated = False
			except HTTPError, e:
				raise TwythonError("endSession failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("You can't end a session when you're not authenticated to begin with.")

	def getDirectMessages(self, since_id = None, max_id = None, count = None, page = "1"):
		"""getDirectMessages(since_id = None, max_id = None, count = None, page = "1")

			Returns a list of the 20 most recent direct messages sent to the authenticating user. 

			Parameters:
				since_id - Optional.  Returns only statuses with an ID greater than (that is, more recent than) the specified ID.
				max_id - Optional.  Returns only statuses with an ID less than (that is, older than) or equal to the specified ID. 
				count - Optional.  Specifies the number of statuses to retrieve. May not be greater than 200.  
				page - Optional. Specifies the page of results to retrieve. Note: there are pagination limits.
		"""
		if self.authenticated is True:
			apiURL = "http://twitter.com/direct_messages.json?page=%s" % `page`
			if since_id is not None:
				apiURL += "&since_id=%s" % `since_id`
			if max_id is not None:
				apiURL += "&max_id=%s" % `max_id`
			if count is not None:
				apiURL += "&count=%s" % `count`

			try:
				return simplejson.load(self.opener.open(apiURL))
			except HTTPError, e:
				raise TwythonError("getDirectMessages() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("getDirectMessages() requires you to be authenticated.")

	def getSentMessages(self, since_id = None, max_id = None, count = None, page = "1"):
		"""getSentMessages(since_id = None, max_id = None, count = None, page = "1")

			Returns a list of the 20 most recent direct messages sent by the authenticating user.

			Parameters:
				since_id - Optional.  Returns only statuses with an ID greater than (that is, more recent than) the specified ID.
				max_id - Optional.  Returns only statuses with an ID less than (that is, older than) or equal to the specified ID. 
				count - Optional.  Specifies the number of statuses to retrieve. May not be greater than 200.  
				page - Optional. Specifies the page of results to retrieve. Note: there are pagination limits.
		"""
		if self.authenticated is True:
			apiURL = "http://twitter.com/direct_messages/sent.json?page=%s" % `page`
			if since_id is not None:
				apiURL += "&since_id=%s" % `since_id`
			if max_id is not None:
				apiURL += "&max_id=%s" % `max_id`
			if count is not None:
				apiURL += "&count=%s" % `count`

			try:
				return simplejson.load(self.opener.open(apiURL))
			except HTTPError, e:
				raise TwythonError("getSentMessages() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("getSentMessages() requires you to be authenticated.")

	def sendDirectMessage(self, user, text):
		"""sendDirectMessage(user, text)

			Sends a new direct message to the specified user from the authenticating user. Requires both the user and text parameters. 
			Returns the sent message in the requested format when successful.

			Parameters:
				user - Required. The ID or screen name of the recipient user.
				text - Required. The text of your direct message. Be sure to keep it under 140 characters.
		"""
		if self.authenticated is True:
			if len(list(text)) < 140:
				try:
					return self.opener.open("http://twitter.com/direct_messages/new.json", urllib.urlencode({"user": user, "text": text}))
				except HTTPError, e:
					raise TwythonError("sendDirectMessage() failed with a %s error code." % `e.code`, e.code)
			else:
				raise TwythonError("Your message must not be longer than 140 characters")
		else:
			raise AuthError("You must be authenticated to send a new direct message.")

	def destroyDirectMessage(self, id):
		"""destroyDirectMessage(id)

			Destroys the direct message specified in the required ID parameter.
			The authenticating user must be the recipient of the specified direct message.

			Parameters:
				id - Required. The ID of the direct message to destroy.
		"""
		if self.authenticated is True:
			try:
				return self.opener.open("http://twitter.com/direct_messages/destroy/%s.json" % id, "")
			except HTTPError, e:
				raise TwythonError("destroyDirectMessage() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("You must be authenticated to destroy a direct message.")

	def createFriendship(self, id = None, user_id = None, screen_name = None, follow = "false"):
		"""createFriendship(id = None, user_id = None, screen_name = None, follow = "false")

			Allows the authenticating users to follow the user specified in the ID parameter.
			Returns the befriended user in the requested format when successful. Returns a
			string describing the failure condition when unsuccessful. If you are already
			friends with the user an HTTP 403 will be returned.

			Parameters:
				** Note: One of the following is required. (id, user_id, screen_name)
				id - Required. The ID or screen name of the user to befriend.
				user_id - Required. Specfies the ID of the user to befriend. Helpful for disambiguating when a valid user ID is also a valid screen name. 
				screen_name - Required. Specfies the screen name of the user to befriend. Helpful for disambiguating when a valid screen name is also a user ID. 
				follow - Optional. Enable notifications for the target user in addition to becoming friends. 
		"""
		if self.authenticated is True:
			apiURL = ""
			if id is not None:
				apiURL = "http://twitter.com/friendships/create/%s.json?follow=%s" %(id, follow)
			if user_id is not None:
				apiURL = "http://twitter.com/friendships/create.json?user_id=%s&follow=%s" %(`user_id`, follow)
			if screen_name is not None:
				apiURL = "http://twitter.com/friendships/create.json?screen_name=%s&follow=%s" %(screen_name, follow)
			try:
				return simplejson.load(self.opener.open(apiURL))
			except HTTPError, e:
				# Rate limiting is done differently here for API reasons...
				if e.code == 403:
					raise TwythonError("You've hit the update limit for this method. Try again in 24 hours.")
				raise TwythonError("createFriendship() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("createFriendship() requires you to be authenticated.")

	def destroyFriendship(self, id = None, user_id = None, screen_name = None):
		"""destroyFriendship(id = None, user_id = None, screen_name = None)

			Allows the authenticating users to unfollow the user specified in the ID parameter.  
			Returns the unfollowed user in the requested format when successful.  Returns a string describing the failure condition when unsuccessful.

			Parameters:
				** Note: One of the following is required. (id, user_id, screen_name)
				id - Required. The ID or screen name of the user to unfollow. 
				user_id - Required. Specfies the ID of the user to unfollow. Helpful for disambiguating when a valid user ID is also a valid screen name. 
				screen_name - Required. Specfies the screen name of the user to unfollow. Helpful for disambiguating when a valid screen name is also a user ID.
		"""
		if self.authenticated is True:
			apiURL = ""
			if id is not None:
				apiURL = "http://twitter.com/friendships/destroy/%s.json" % id
			if user_id is not None:
				apiURL = "http://twitter.com/friendships/destroy.json?user_id=%s" %	`user_id`
			if screen_name is not None:
				apiURL = "http://twitter.com/friendships/destroy.json?screen_name=%s" % screen_name
			try:
				return simplejson.load(self.opener.open(apiURL))
			except HTTPError, e:
				raise TwythonError("destroyFriendship() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("destroyFriendship() requires you to be authenticated.")

	def checkIfFriendshipExists(self, user_a, user_b):
		"""checkIfFriendshipExists(user_a, user_b)

			Tests for the existence of friendship between two users.
			Will return true if user_a follows user_b; otherwise, it'll return false.

			Parameters:
				user_a - Required. The ID or screen_name of the subject user.
				user_b - Required. The ID or screen_name of the user to test for following.
		"""
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/friendships/exists.json", urllib.urlencode({"user_a": user_a, "user_b": user_b})))
			except HTTPError, e:
				raise TwythonError("checkIfFriendshipExists() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("checkIfFriendshipExists(), oddly, requires that you be authenticated.")

	def updateDeliveryDevice(self, device_name = "none"):
		"""updateDeliveryDevice(device_name = "none")

			Sets which device Twitter delivers updates to for the authenticating user.
			Sending "none" as the device parameter will disable IM or SMS updates. (Simply calling .updateDeliveryService() also accomplishes this)

			Parameters:
				device - Required. Must be one of: sms, im, none.
		"""
		if self.authenticated is True:
			try:
				return self.opener.open("http://twitter.com/account/update_delivery_device.json?", urllib.urlencode({"device": self.unicode2utf8(device_name)}))
			except HTTPError, e:
				raise TwythonError("updateDeliveryDevice() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("updateDeliveryDevice() requires you to be authenticated.")

	def updateProfileColors(self, **kwargs):
		"""updateProfileColors(**kwargs)

			Sets one or more hex values that control the color scheme of the authenticating user's profile page on twitter.com.

			Parameters:
				** Note: One or more of the following parameters must be present. Each parameter's value must
				be a valid hexidecimal value, and may be either three or six characters (ex: #fff or #ffffff).

				profile_background_color - Optional.
				profile_text_color - Optional.
				profile_link_color - Optional.
				profile_sidebar_fill_color - Optional.
				profile_sidebar_border_color - Optional.
		"""
		if self.authenticated is True:
			try:
				return self.opener.open(self.constructApiURL("http://twitter.com/account/update_profile_colors.json?", kwargs))
			except HTTPError, e:
				raise TwythonError("updateProfileColors() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("updateProfileColors() requires you to be authenticated.")

	def updateProfile(self, name = None, email = None, url = None, location = None, description = None):
		"""updateProfile(name = None, email = None, url = None, location = None, description = None)

			Sets values that users are able to set under the "Account" tab of their settings page. 
			Only the parameters specified will be updated.

			Parameters:
				One or more of the following parameters must be present.  Each parameter's value
				should be a string.  See the individual parameter descriptions below for further constraints.

				name - Optional. Maximum of 20 characters.
				email - Optional. Maximum of 40 characters. Must be a valid email address.
				url - Optional. Maximum of 100 characters. Will be prepended with "http://" if not present.
				location - Optional. Maximum of 30 characters. The contents are not normalized or geocoded in any way.
				description - Optional. Maximum of 160 characters.
		"""
		if self.authenticated is True:
			useAmpersands = False
			updateProfileQueryString = ""
			if name is not None:
				if len(list(name)) < 20:
					updateProfileQueryString += "name=" + name
					useAmpersands = True
				else:
					raise TwythonError("Twitter has a character limit of 20 for all usernames. Try again.")
			if email is not None and "@" in email:
				if len(list(email)) < 40:
					if useAmpersands is True:
						updateProfileQueryString += "&email=" + email
					else:
						updateProfileQueryString += "email=" + email
						useAmpersands = True
				else:
					raise TwythonError("Twitter has a character limit of 40 for all email addresses, and the email address must be valid. Try again.")
			if url is not None:
				if len(list(url)) < 100:
					if useAmpersands is True:
						updateProfileQueryString += "&" + urllib.urlencode({"url": self.unicode2utf8(url)})
					else:
						updateProfileQueryString += urllib.urlencode({"url": self.unicode2utf8(url)})
						useAmpersands = True
				else:
					raise TwythonError("Twitter has a character limit of 100 for all urls. Try again.")
			if location is not None:
				if len(list(location)) < 30:
					if useAmpersands is True:
						updateProfileQueryString += "&" + urllib.urlencode({"location": self.unicode2utf8(location)})
					else:
						updateProfileQueryString += urllib.urlencode({"location": self.unicode2utf8(location)})
						useAmpersands = True
				else:
					raise TwythonError("Twitter has a character limit of 30 for all locations. Try again.")
			if description is not None:
				if len(list(description)) < 160:
					if useAmpersands is True:
						updateProfileQueryString += "&" + urllib.urlencode({"description": self.unicode2utf8(description)})
					else:
						updateProfileQueryString += urllib.urlencode({"description": self.unicode2utf8(description)})
				else:
					raise TwythonError("Twitter has a character limit of 160 for all descriptions. Try again.")

			if updateProfileQueryString != "":
				try:
					return self.opener.open("http://twitter.com/account/update_profile.json?", updateProfileQueryString)
				except HTTPError, e:
					raise TwythonError("updateProfile() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("updateProfile() requires you to be authenticated.")

	def getFavorites(self, page = "1"):
		"""getFavorites(page = "1")

			Returns the 20 most recent favorite statuses for the authenticating user or user specified by the ID parameter in the requested format.

			Parameters:
				page - Optional. Specifies the page of favorites to retrieve.
		"""
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/favorites.json?page=%s" % `page`))
			except HTTPError, e:
				raise TwythonError("getFavorites() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("getFavorites() requires you to be authenticated.")

	def createFavorite(self, id):
		"""createFavorite(id)

			Favorites the status specified in the ID parameter as the authenticating user. Returns the favorite status when successful.

			Parameters:
				id - Required. The ID of the status to favorite.
		"""
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/favorites/create/%s.json" % `id`, ""))
			except HTTPError, e:
				raise TwythonError("createFavorite() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("createFavorite() requires you to be authenticated.")

	def destroyFavorite(self, id):
		"""destroyFavorite(id)

			Un-favorites the status specified in the ID parameter as the authenticating user. Returns the un-favorited status in the requested format when successful.

			Parameters:
				id - Required. The ID of the status to un-favorite.
		"""
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/favorites/destroy/%s.json" % `id`, ""))
			except HTTPError, e:
				raise TwythonError("destroyFavorite() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("destroyFavorite() requires you to be authenticated.")

	def notificationFollow(self, id = None, user_id = None, screen_name = None):
		"""notificationFollow(id = None, user_id = None, screen_name = None)

			Enables device notifications for updates from the specified user. Returns the specified user when successful.

			Parameters:
				** Note: One of the following is required. (id, user_id, screen_name)
				id - Required. The ID or screen name of the user to follow with device updates.
				user_id - Required. Specfies the ID of the user to follow with device updates. Helpful for disambiguating when a valid user ID is also a valid screen name. 
				screen_name - Required. Specfies the screen name of the user to follow with device updates. Helpful for disambiguating when a valid screen name is also a user ID. 
		"""
		if self.authenticated is True:
			apiURL = ""
			if id is not None:
				apiURL = "http://twitter.com/notifications/follow/%s.json" % id
			if user_id is not None:
				apiURL = "http://twitter.com/notifications/follow/follow.json?user_id=%s" % `user_id`
			if screen_name is not None:
				apiURL = "http://twitter.com/notifications/follow/follow.json?screen_name=%s" % screen_name
			try:
				return simplejson.load(self.opener.open(apiURL, ""))
			except HTTPError, e:
				raise TwythonError("notificationFollow() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("notificationFollow() requires you to be authenticated.")

	def notificationLeave(self, id = None, user_id = None, screen_name = None):
		"""notificationLeave(id = None, user_id = None, screen_name = None)

			Disables notifications for updates from the specified user to the authenticating user.  Returns the specified user when successful.

			Parameters:
				** Note: One of the following is required. (id, user_id, screen_name)
				id - Required. The ID or screen name of the user to follow with device updates.
				user_id - Required. Specfies the ID of the user to follow with device updates. Helpful for disambiguating when a valid user ID is also a valid screen name. 
				screen_name - Required. Specfies the screen name of the user to follow with device updates. Helpful for disambiguating when a valid screen name is also a user ID. 
		"""
		if self.authenticated is True:
			apiURL = ""
			if id is not None:
				apiURL = "http://twitter.com/notifications/leave/%s.json" % id
			if user_id is not None:
				apiURL = "http://twitter.com/notifications/leave/leave.json?user_id=%s" % `user_id`
			if screen_name is not None:
				apiURL = "http://twitter.com/notifications/leave/leave.json?screen_name=%s" % screen_name
			try:
				return simplejson.load(self.opener.open(apiURL, ""))
			except HTTPError, e:
				raise TwythonError("notificationLeave() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("notificationLeave() requires you to be authenticated.")

	def getFriendsIDs(self, id = None, user_id = None, screen_name = None, page = "1"):
		"""getFriendsIDs(id = None, user_id = None, screen_name = None, page = "1")

			Returns an array of numeric IDs for every user the specified user is following.

			Parameters:
				** Note: One of the following is required. (id, user_id, screen_name)
				id - Required. The ID or screen name of the user to follow with device updates.
				user_id - Required. Specfies the ID of the user to follow with device updates. Helpful for disambiguating when a valid user ID is also a valid screen name. 
				screen_name - Required. Specfies the screen name of the user to follow with device updates. Helpful for disambiguating when a valid screen name is also a user ID. 
				page - Optional. Specifies the page number of the results beginning at 1. A single page contains up to 5000 ids. This is recommended for users with large ID lists. If not provided all ids are returned. (Please note that the result set isn't guaranteed to be 5000 every time as suspended users will be filtered out.)
		"""
		apiURL = ""
		if id is not None:
			apiURL = "http://twitter.com/friends/ids/%s.json?page=%s" %(id, `page`)
		if user_id is not None:
			apiURL = "http://twitter.com/friends/ids.json?user_id=%s&page=%s" %(`user_id`, `page`)
		if screen_name is not None:
			apiURL = "http://twitter.com/friends/ids.json?screen_name=%s&page=%s" %(screen_name, `page`)
		try:
			return simplejson.load(urllib2.urlopen(apiURL))
		except HTTPError, e:
			raise TwythonError("getFriendsIDs() failed with a %s error code." % `e.code`, e.code)

	def getFollowersIDs(self, id = None, user_id = None, screen_name = None, page = "1"):
		"""getFollowersIDs(id = None, user_id = None, screen_name = None, page = "1")

			Returns an array of numeric IDs for every user following the specified user.

			Parameters:
				** Note: One of the following is required. (id, user_id, screen_name)
				id - Required. The ID or screen name of the user to follow with device updates.
				user_id - Required. Specfies the ID of the user to follow with device updates. Helpful for disambiguating when a valid user ID is also a valid screen name. 
				screen_name - Required. Specfies the screen name of the user to follow with device updates. Helpful for disambiguating when a valid screen name is also a user ID. 
				page - Optional. Specifies the page number of the results beginning at 1. A single page contains 5000 ids. This is recommended for users with large ID lists. If not provided all ids are returned. (Please note that the result set isn't guaranteed to be 5000 every time as suspended users will be filtered out.)
		"""
		apiURL = ""
		if id is not None:
			apiURL = "http://twitter.com/followers/ids/%s.json?page=%s" %(`id`, `page`)
		if user_id is not None:
			apiURL = "http://twitter.com/followers/ids.json?user_id=%s&page=%s" %(`user_id`, `page`)
		if screen_name is not None:
			apiURL = "http://twitter.com/followers/ids.json?screen_name=%s&page=%s" %(screen_name, `page`)
		try:
			return simplejson.load(urllib2.urlopen(apiURL))
		except HTTPError, e:
			raise TwythonError("getFollowersIDs() failed with a %s error code." % `e.code`, e.code)

	def createBlock(self, id):
		"""createBlock(id)

			Blocks the user specified in the ID parameter as the authenticating user. Destroys a friendship to the blocked user if it exists. 
			Returns the blocked user in the requested format when successful.

			Parameters:
				id - The ID or screen name of a user to block.
		"""
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/blocks/create/%s.json" % `id`, ""))
			except HTTPError, e:
				raise TwythonError("createBlock() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("createBlock() requires you to be authenticated.")

	def destroyBlock(self, id):
		"""destroyBlock(id)

			Un-blocks the user specified in the ID parameter for the authenticating user.
			Returns the un-blocked user in the requested format when successful.

			Parameters:
				id - Required. The ID or screen_name of the user to un-block
		"""
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/blocks/destroy/%s.json" % `id`, ""))
			except HTTPError, e:
				raise TwythonError("destroyBlock() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("destroyBlock() requires you to be authenticated.")

	def checkIfBlockExists(self, id = None, user_id = None, screen_name = None):
		"""checkIfBlockExists(id = None, user_id = None, screen_name = None)

			Returns if the authenticating user is blocking a target user. Will return the blocked user's object if a block exists, and 
			error with an HTTP 404 response code otherwise.

			Parameters:
				** Note: One of the following is required. (id, user_id, screen_name)
				id - Optional. The ID or screen_name of the potentially blocked user.
				user_id - Optional. Specfies the ID of the potentially blocked user. Helpful for disambiguating when a valid user ID is also a valid screen name.
				screen_name - Optional. Specfies the screen name of the potentially blocked user. Helpful for disambiguating when a valid screen name is also a user ID.
		"""
		apiURL = ""
		if id is not None:
			apiURL = "http://twitter.com/blocks/exists/%s.json" % `id`
		if user_id is not None:
			apiURL = "http://twitter.com/blocks/exists.json?user_id=%s" % `user_id`
		if screen_name is not None:
			apiURL = "http://twitter.com/blocks/exists.json?screen_name=%s" % screen_name
		try:
			return simplejson.load(urllib2.urlopen(apiURL))
		except HTTPError, e:
			raise TwythonError("checkIfBlockExists() failed with a %s error code." % `e.code`, e.code)

	def getBlocking(self, page = "1"):
		"""getBlocking(page = "1")

			Returns an array of user objects that the authenticating user is blocking.

			Parameters:
				page - Optional. Specifies the page number of the results beginning at 1. A single page contains 20 ids.
		"""
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/blocks/blocking.json?page=%s" % `page`))
			except HTTPError, e:
				raise TwythonError("getBlocking() failed with a %s error code." %	`e.code`, e.code)
		else:
			raise AuthError("getBlocking() requires you to be authenticated")

	def getBlockedIDs(self):
		"""getBlockedIDs()

			Returns an array of numeric user ids the authenticating user is blocking.
		"""
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/blocks/blocking/ids.json"))
			except HTTPError, e:
				raise TwythonError("getBlockedIDs() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("getBlockedIDs() requires you to be authenticated.")

	def searchTwitter(self, search_query, **kwargs):
		"""searchTwitter(search_query, **kwargs)

			Returns tweets that match a specified query.

			Parameters:
				callback - Optional. Only available for JSON format. If supplied, the response will use the JSONP format with a callback of the given name.
				lang - Optional. Restricts tweets to the given language, given by an ISO 639-1 code.
				locale - Optional. Language of the query you're sending (only ja is currently effective). Intended for language-specific clients; default should work in most cases.
				rpp - Optional. The number of tweets to return per page, up to a max of 100.
				page - Optional. The page number (starting at 1) to return, up to a max of roughly 1500 results (based on rpp * page. Note: there are pagination limits.)
				since_id - Optional. Returns tweets with status ids greater than the given id.
				geocode - Optional. Returns tweets by users located within a given radius of the given latitude/longitude, where the user's location is taken from their Twitter profile. The parameter value is specified by "latitide,longitude,radius", where radius units must be specified as either "mi" (miles) or "km" (kilometers). Note that you cannot use the near operator via the API to geocode arbitrary locations; however you can use this geocode parameter to search near geocodes directly.
				show_user - Optional. When true, prepends "<user>:" to the beginning of the tweet. This is useful for readers that do not display Atom's author field. The default is false. 

			Usage Notes:
				Queries are limited 140 URL encoded characters.
				Some users may be absent from search results.
				The since_id parameter will be removed from the next_page element as it is not supported for pagination. If since_id is removed a warning will be added to alert you.
				This method will return an HTTP 404 error if since_id is used and is too old to be in the search index.
				
			Applications must have a meaningful and unique User Agent when using this method. 
			An HTTP Referrer is expected but not required. Search traffic that does not include a User Agent will be rate limited to fewer API calls per hour than 
			applications including a User Agent string. You can set your custom UA headers by passing it as a respective argument to the setup() method.
		"""
		searchURL = self.constructApiURL("http://search.twitter.com/search.json", kwargs) + "&" + urllib.urlencode({"q": self.unicode2utf8(search_query)})
		try:
			return simplejson.load(urllib2.urlopen(searchURL))
		except HTTPError, e:
			raise TwythonError("getSearchTimeline() failed with a %s error code." % `e.code`, e.code)

	def getCurrentTrends(self, excludeHashTags = False):
		"""getCurrentTrends(excludeHashTags = False)

			Returns the current top 10 trending topics on Twitter.  The response includes the time of the request, the name of each trending topic, and the query used 
			on Twitter Search results page for that topic.

			Parameters:
				excludeHashTags - Optional. Setting this equal to hashtags will remove all hashtags from the trends list.
		"""
		apiURL = "http://search.twitter.com/trends/current.json"
		if excludeHashTags is True:
			apiURL += "?exclude=hashtags"
		try:
			return simplejson.load(urllib.urlopen(apiURL))
		except HTTPError, e:
			raise TwythonError("getCurrentTrends() failed with a %s error code." % `e.code`, e.code)

	def getDailyTrends(self, date = None, exclude = False):
		"""getDailyTrends(date = None, exclude = False)

			Returns the top 20 trending topics for each hour in a given day.

			Parameters:
				date - Optional. Permits specifying a start date for the report. The date should be formatted YYYY-MM-DD.
				exclude - Optional. Setting this equal to hashtags will remove all hashtags from the trends list.
		"""
		apiURL = "http://search.twitter.com/trends/daily.json"
		questionMarkUsed = False
		if date is not None:
			apiURL += "?date=%s" % date
			questionMarkUsed = True
		if exclude is True:
			if questionMarkUsed is True:
				apiURL += "&exclude=hashtags"
			else:
				apiURL += "?exclude=hashtags"
		try:
			return simplejson.load(urllib.urlopen(apiURL))
		except HTTPError, e:
			raise TwythonError("getDailyTrends() failed with a %s error code." % `e.code`, e.code)

	def getWeeklyTrends(self, date = None, exclude = False):
		"""getWeeklyTrends(date = None, exclude = False)

			Returns the top 30 trending topics for each day in a given week.

			Parameters:
				date - Optional. Permits specifying a start date for the report. The date should be formatted YYYY-MM-DD.
				exclude - Optional. Setting this equal to hashtags will remove all hashtags from the trends list.
		"""
		apiURL = "http://search.twitter.com/trends/daily.json"
		questionMarkUsed = False
		if date is not None:
			apiURL += "?date=%s" % date
			questionMarkUsed = True
		if exclude is True:
			if questionMarkUsed is True:
				apiURL += "&exclude=hashtags"
			else:
				apiURL += "?exclude=hashtags"
		try:
			return simplejson.load(urllib.urlopen(apiURL))
		except HTTPError, e:
			raise TwythonError("getWeeklyTrends() failed with a %s error code." % `e.code`, e.code)

	def getSavedSearches(self):
		"""getSavedSearches()

			Returns the authenticated user's saved search queries.
		"""
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/saved_searches.json"))
			except HTTPError, e:
				raise TwythonError("getSavedSearches() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("getSavedSearches() requires you to be authenticated.")

	def showSavedSearch(self, id):
		"""showSavedSearch(id)

			Retrieve the data for a saved search owned by the authenticating user specified by the given id.

			Parameters:
				id - Required. The id of the saved search to be retrieved.
		"""
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/saved_searches/show/%s.json" % `id`))
			except HTTPError, e:
				raise TwythonError("showSavedSearch() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("showSavedSearch() requires you to be authenticated.")

	def createSavedSearch(self, query):
		"""createSavedSearch(query)

			Creates a saved search for the authenticated user.

			Parameters:
				query - Required. The query of the search the user would like to save.
		"""
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/saved_searches/create.json?query=%s" % query, ""))
			except HTTPError, e:
				raise TwythonError("createSavedSearch() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("createSavedSearch() requires you to be authenticated.")

	def destroySavedSearch(self, id):
		"""destroySavedSearch(id)

			Destroys a saved search for the authenticated user.
			The search specified by id must be owned by the authenticating user.

			Parameters:
				id - Required. The id of the saved search to be deleted.
		"""
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/saved_searches/destroy/%s.json" % `id`, ""))
			except HTTPError, e:
				raise TwythonError("destroySavedSearch() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("destroySavedSearch() requires you to be authenticated.")

	# The following methods are apart from the other Account methods, because they rely on a whole multipart-data posting function set.
	def updateProfileBackgroundImage(self, filename, tile="true"):
		"""updateProfileBackgroundImage(filename, tile="true")

			Updates the authenticating user's profile background image.

			Parameters:
				image - Required. Must be a valid GIF, JPG, or PNG image of less than 800 kilobytes in size. Images with width larger than 2048 pixels will be forceably scaled down.
				tile - Optional (defaults to true). If set to true the background image will be displayed tiled. The image will not be tiled otherwise. 
				** Note: It's sad, but when using this method, pass the tile value as a string, e.g tile="false"
		"""
		if self.authenticated is True:
			try:
				files = [("image", filename, open(filename).read())]
				fields = []
				content_type, body = self.encode_multipart_formdata(fields, files)
				headers = {'Content-Type': content_type, 'Content-Length': str(len(body))}
				r = urllib2.Request("http://twitter.com/account/update_profile_background_image.json?tile=" + tile, body, headers)
				return self.opener.open(r).read()
			except HTTPError, e:
				raise TwythonError("updateProfileBackgroundImage() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("You realize you need to be authenticated to change a background image, right?")

	def updateProfileImage(self, filename):
		"""updateProfileImage(filename)

			Updates the authenticating user's profile image (avatar).

			Parameters:
				image - Required. Must be a valid GIF, JPG, or PNG image of less than 700 kilobytes in size. Images with width larger than 500 pixels will be scaled down.
		"""
		if self.authenticated is True:
			try:
				files = [("image", filename, open(filename).read())]
				fields = []
				content_type, body = self.encode_multipart_formdata(fields, files)
				headers = {'Content-Type': content_type, 'Content-Length': str(len(body))}
				r = urllib2.Request("http://twitter.com/account/update_profile_image.json", body, headers)
				return self.opener.open(r).read()
			except HTTPError, e:
				raise TwythonError("updateProfileImage() failed with a %s error code." % `e.code`, e.code)
		else:
			raise AuthError("You realize you need to be authenticated to change a profile image, right?")

	def encode_multipart_formdata(self, fields, files):
		BOUNDARY = mimetools.choose_boundary()
		CRLF = '\r\n'
		L = []
		for (key, value) in fields:
			L.append('--' + BOUNDARY)
			L.append('Content-Disposition: form-data; name="%s"' % key)
			L.append('')
			L.append(value)
		for (key, filename, value) in files:
			L.append('--' + BOUNDARY)
			L.append('Content-Disposition: form-data; name="%s"; filename="%s"' % (key, filename))
			L.append('Content-Type: %s' % self.get_content_type(filename))
			L.append('')
			L.append(value)
		L.append('--' + BOUNDARY + '--')
		L.append('')
		body = CRLF.join(L)
		content_type = 'multipart/form-data; boundary=%s' % BOUNDARY
		return content_type, body

	def get_content_type(self, filename):
		return mimetypes.guess_type(filename)[0] or 'application/octet-stream'

	def unicode2utf8(self, text):
		try:
			if isinstance(text, unicode):
				text = text.encode('utf-8')
		except:
			pass
		return text
