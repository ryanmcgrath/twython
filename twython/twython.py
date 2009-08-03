#!/usr/bin/python

"""
    NOTE: Tango is being renamed to Twython; all basic strings have been changed below, but there's still work ongoing in this department.

	Twython is an up-to-date library for Python that wraps the Twitter API.
	Other Python Twitter libraries seem to have fallen a bit behind, and
	Twitter's API has evolved a bit. Here's hoping this helps.

	TODO: OAuth, Streaming API?

	Questions, comments? ryan@venodesigns.net
"""

import httplib, urllib, urllib2, mimetypes, mimetools

from urllib2 import HTTPError

__author__ = "Ryan McGrath <ryan@venodesigns.net>"
__version__ = "0.8.0.1"

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

class TangoError(Exception):
	def __init__(self, msg, error_code=None):
		self.msg = msg
		if error_code == 400:
			raise APILimit(msg)
	def __str__(self):
		return repr(self.msg)

class APILimit(TangoError):
	def __init__(self, msg):
		self.msg = msg
	def __str__(self):
		return repr(self.msg)

class setup:
	def __init__(self, authtype = "OAuth", username = None, password = None, oauth_keys = None, headers = None):
		self.authtype = authtype
		self.authenticated = False
		self.username = username
		self.password = password
		self.oauth_keys = oauth_keys
		if self.username is not None and self.password is not None:
			if self.authtype == "OAuth":
				self.request_token_url = 'https://twitter.com/oauth/request_token'
				self.access_token_url = 'https://twitter.com/oauth/access_token'
				self.authorization_url = 'http://twitter.com/oauth/authorize'
				self.signin_url = 'http://twitter.com/oauth/authenticate'
				# Do OAuth type stuff here - how should this be handled? Seems like a framework question...
			elif self.authtype == "Basic":
				self.auth_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
				self.auth_manager.add_password(None, "http://twitter.com", self.username, self.password)
				self.handler = urllib2.HTTPBasicAuthHandler(self.auth_manager)
				self.opener = urllib2.build_opener(self.handler)
				if headers is not None:
					self.opener.addheaders = [('User-agent', headers)]
				try:
					simplejson.load(self.opener.open("http://twitter.com/account/verify_credentials.json"))
					self.authenticated = True
				except HTTPError, e:
					raise TangoError("Authentication failed with your provided credentials. Try again? (%s failure)" % `e.code`, e.code)
	
	# OAuth functions; shortcuts for verifying the credentials.
	def fetch_response_oauth(self, oauth_request):
		pass
	
	def get_unauthorized_request_token(self):
		pass
	
	def get_authorization_url(self, token):
		pass
	
	def exchange_tokens(self, request_token):
		pass
	
	# URL Shortening function huzzah
	def shortenURL(self, url_to_shorten, shortener = "http://is.gd/api.php", query = "longurl"):
		try:
			return urllib2.urlopen(shortener + "?" + urllib.urlencode({query: url_to_shorten})).read()
		except HTTPError, e:
			raise TangoError("shortenURL() failed with a %s error code." % `e.code`)
	
	def constructApiURL(self, base_url, params):
		return base_url + "?" + "&".join(["%s=%s" %(key, value) for (key, value) in params.iteritems()])
	
	def getRateLimitStatus(self, rate_for = "requestingIP"):
		try:
			if rate_for == "requestingIP":
				return simplejson.load(urllib2.urlopen("http://twitter.com/account/rate_limit_status.json"))
			else:
				if self.authenticated is True:
					return simplejson.load(self.opener.open("http://twitter.com/account/rate_limit_status.json"))
				else:
					raise TangoError("You need to be authenticated to check a rate limit status on an account.")
		except HTTPError, e:
			raise TangoError("It seems that there's something wrong. Twitter gave you a %s error code; are you doing something you shouldn't be?" % `e.code`, e.code)
	
	def getPublicTimeline(self):
		try:
			return simplejson.load(urllib2.urlopen("http://twitter.com/statuses/public_timeline.json"))
		except HTTPError, e:
			raise TangoError("getPublicTimeline() failed with a %s error code." % `e.code`)
	
	def getFriendsTimeline(self, **kwargs):
		if self.authenticated is True:
			try:
				friendsTimelineURL = self.constructApiURL("http://twitter.com/statuses/friends_timeline.json", kwargs)
				return simplejson.load(self.opener.open(friendsTimelineURL))
			except HTTPError, e:
				raise TangoError("getFriendsTimeline() failed with a %s error code." % `e.code`)
		else:
			raise TangoError("getFriendsTimeline() requires you to be authenticated.")
	
	def getUserTimeline(self, id = None, **kwargs): 
		if id is not None and kwargs.has_key("user_id") is False and kwargs.has_key("screen_name") is False:
			userTimelineURL = self.constructApiURL("http://twitter.com/statuses/user_timeline/" + id + ".json", kwargs)
		elif id is None and kwargs.has_key("user_id") is False and kwargs.has_key("screen_name") is False and self.authenticated is True:
			userTimelineURL = self.constructApiURL("http://twitter.com/statuses/user_timeline/" + self.username + ".json", kwargs)
		else:
			userTimelineURL = self.constructApiURL("http://twitter.com/statuses/user_timeline.json", kwargs)
		try:
			# We do our custom opener if we're authenticated, as it helps avoid cases where it's a protected user
			if self.authenticated is True:
				return simplejson.load(self.opener.open(userTimelineURL))
			else:
				return simplejson.load(urllib2.urlopen(userTimelineURL))
		except HTTPError, e:
			raise TangoError("Failed with a %s error code. Does this user hide/protect their updates? If so, you'll need to authenticate and be their friend to get their timeline."
				% `e.code`, e.code)
	
	def getUserMentions(self, **kwargs):
		if self.authenticated is True:
			try:
				mentionsFeedURL = self.constructApiURL("http://twitter.com/statuses/mentions.json", kwargs)
				return simplejson.load(self.opener.open(mentionsFeedURL))
			except HTTPError, e:
				raise TangoError("getUserMentions() failed with a %s error code." % `e.code`, e.code)
		else:
			raise TangoError("getUserMentions() requires you to be authenticated.")
	
	def showStatus(self, id):
		try:
			if self.authenticated is True:
				return simplejson.load(self.opener.open("http://twitter.com/statuses/show/%s.json" % id))
			else:
				return simplejson.load(urllib2.urlopen("http://twitter.com/statuses/show/%s.json" % id))
		except HTTPError, e:
			raise TangoError("Failed with a %s error code. Does this user hide/protect their updates? You'll need to authenticate and be friends to get their timeline." 
				% `e.code`, e.code)
	
	def updateStatus(self, status, in_reply_to_status_id = None):
		if self.authenticated is True:
			if len(list(status)) > 140:
				raise TangoError("This status message is over 140 characters. Trim it down!")
			try:
				return simplejson.load(self.opener.open("http://twitter.com/statuses/update.json?", urllib.urlencode({"status": status, "in_reply_to_status_id": in_reply_to_status_id})))
			except HTTPError, e:
				raise TangoError("updateStatus() failed with a %s error code." % `e.code`, e.code)
		else:
			raise TangoError("updateStatus() requires you to be authenticated.")
	
	def destroyStatus(self, id):
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/status/destroy/%s.json", "POST" % id))
			except HTTPError, e:
				raise TangoError("destroyStatus() failed with a %s error code." % `e.code`, e.code)
		else:
			raise TangoError("destroyStatus() requires you to be authenticated.")
	
	def endSession(self):
		if self.authenticated is True:
			try:
				self.opener.open("http://twitter.com/account/end_session.json", "")
				self.authenticated = False
			except HTTPError, e:
				raise TangoError("endSession failed with a %s error code." % `e.code`, e.code)
		else:
			raise TangoError("You can't end a session when you're not authenticated to begin with.")
	
	def getDirectMessages(self, since_id = None, max_id = None, count = None, page = "1"):
		if self.authenticated is True:
			apiURL = "http://twitter.com/direct_messages.json?page=" + page
			if since_id is not None:
				apiURL += "&since_id=" + since_id
			if max_id is not None:
				apiURL += "&max_id=" + max_id
			if count is not None:
				apiURL += "&count=" + count
			
			try:
				return simplejson.load(self.opener.open(apiURL))
			except HTTPError, e:
				raise TangoError("getDirectMessages() failed with a %s error code." % `e.code`, e.code)
		else:
			raise TangoError("getDirectMessages() requires you to be authenticated.")
	
	def getSentMessages(self, since_id = None, max_id = None, count = None, page = "1"):
		if self.authenticated is True:
			apiURL = "http://twitter.com/direct_messages/sent.json?page=" + page
			if since_id is not None:
				apiURL += "&since_id=" + since_id
			if max_id is not None:
				apiURL += "&max_id=" + max_id
			if count is not None:
				apiURL += "&count=" + count
			
			try:
				return simplejson.load(self.opener.open(apiURL))
			except HTTPError, e:
				raise TangoError("getSentMessages() failed with a %s error code." % `e.code`, e.code)
		else:
			raise TangoError("getSentMessages() requires you to be authenticated.")
	
	def sendDirectMessage(self, user, text):
		if self.authenticated is True:
			if len(list(text)) < 140:
				try:
					return self.opener.open("http://twitter.com/direct_messages/new.json", urllib.urlencode({"user": user, "text": text}))
				except HTTPError, e:
					raise TangoError("sendDirectMessage() failed with a %s error code." % `e.code`, e.code)
			else:
				raise TangoError("Your message must not be longer than 140 characters")
		else:
			raise TangoError("You must be authenticated to send a new direct message.")
	
	def destroyDirectMessage(self, id):
		if self.authenticated is True:
			try:
				return self.opener.open("http://twitter.com/direct_messages/destroy/%s.json" % id, "")
			except HTTPError, e:
				raise TangoError("destroyDirectMessage() failed with a %s error code." % `e.code`, e.code)
		else:
			raise TangoError("You must be authenticated to destroy a direct message.")
	
	def createFriendship(self, id = None, user_id = None, screen_name = None, follow = "false"):
		if self.authenticated is True:
			apiURL = ""
			if id is not None:
				apiURL = "http://twitter.com/friendships/create/" + id + ".json" + "?follow=" + follow
			if user_id is not None:
				apiURL = "http://twitter.com/friendships/create.json?user_id=" + user_id + "&follow=" + follow
			if screen_name is not None:
				apiURL = "http://twitter.com/friendships/create.json?screen_name=" + screen_name + "&follow=" + follow
			try:
				return simplejson.load(self.opener.open(apiURL))
			except HTTPError, e:
				# Rate limiting is done differently here for API reasons...
				if e.code == 403:
					raise TangoError("You've hit the update limit for this method. Try again in 24 hours.")
				raise TangoError("createFriendship() failed with a %s error code." % `e.code`, e.code)
		else:
			raise TangoError("createFriendship() requires you to be authenticated.")
		
	def destroyFriendship(self, id = None, user_id = None, screen_name = None):
		if self.authenticated is True:
			apiURL = ""
			if id is not None:
				apiURL = "http://twitter.com/friendships/destroy/" + id + ".json"
			if user_id is not None:
				apiURL = "http://twitter.com/friendships/destroy.json?user_id=" + user_id
			if screen_name is not None:
				apiURL = "http://twitter.com/friendships/destroy.json?screen_name=" + screen_name
			try:
				return simplejson.load(self.opener.open(apiURL))
			except HTTPError, e:
				raise TangoError("destroyFriendship() failed with a %s error code." % `e.code`, e.code)
		else:
			raise TangoError("destroyFriendship() requires you to be authenticated.")
	
	def checkIfFriendshipExists(self, user_a, user_b):
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/friendships/exists.json", urllib.urlencode({"user_a": user_a, "user_b": user_b})))
			except HTTPError, e:
				raise TangoError("checkIfFriendshipExists() failed with a %s error code." % `e.code`, e.code)
		else:
			raise TangoError("checkIfFriendshipExists(), oddly, requires that you be authenticated.")
	
	def updateDeliveryDevice(self, device_name = "none"):
		if self.authenticated is True:
			try:
				return self.opener.open("http://twitter.com/account/update_delivery_device.json?", urllib.urlencode({"device": device_name}))
			except HTTPError, e:
				raise TangoError("updateDeliveryDevice() failed with a %s error code." % `e.code`, e.code)
		else:
			raise TangoError("updateDeliveryDevice() requires you to be authenticated.")
	
	def updateProfileColors(self, **kwargs):
		if self.authenticated is True:
			try:
				return self.opener.open(self.constructApiURL("http://twitter.com/account/update_profile_colors.json?", kwargs))
			except HTTPError, e:
				raise TangoError("updateProfileColors() failed with a %s error code." % `e.code`, e.code)
		else:
			raise TangoError("updateProfileColors() requires you to be authenticated.")
	
	def updateProfile(self, name = None, email = None, url = None, location = None, description = None):
		if self.authenticated is True:
			useAmpersands = False
			updateProfileQueryString = ""
			if name is not None:
				if len(list(name)) < 20:
					updateProfileQueryString += "name=" + name
					useAmpersands = True
				else:
					raise TangoError("Twitter has a character limit of 20 for all usernames. Try again.")
			if email is not None and "@" in email:
				if len(list(email)) < 40:
					if useAmpersands is True:
						updateProfileQueryString += "&email=" + email
					else:
						updateProfileQueryString += "email=" + email
						useAmpersands = True
				else:
					raise TangoError("Twitter has a character limit of 40 for all email addresses, and the email address must be valid. Try again.")
			if url is not None:
				if len(list(url)) < 100:
					if useAmpersands is True:
						updateProfileQueryString += "&" + urllib.urlencode({"url": url})
					else:
						updateProfileQueryString += urllib.urlencode({"url": url})
						useAmpersands = True
				else:
					raise TangoError("Twitter has a character limit of 100 for all urls. Try again.")
			if location is not None:
				if len(list(location)) < 30:
					if useAmpersands is True:
						updateProfileQueryString += "&" + urllib.urlencode({"location": location})
					else:
						updateProfileQueryString += urllib.urlencode({"location": location})
						useAmpersands = True
				else:
					raise TangoError("Twitter has a character limit of 30 for all locations. Try again.")
			if description is not None:
				if len(list(description)) < 160:
					if useAmpersands is True:
						updateProfileQueryString += "&" + urllib.urlencode({"description": description})
					else:
						updateProfileQueryString += urllib.urlencode({"description": description})
				else:
					raise TangoError("Twitter has a character limit of 160 for all descriptions. Try again.")
			
			if updateProfileQueryString != "":
				try:
					return self.opener.open("http://twitter.com/account/update_profile.json?", updateProfileQueryString)
				except HTTPError, e:
					raise TangoError("updateProfile() failed with a %s error code." % `e.code`, e.code)
		else:
			raise TangoError("updateProfile() requires you to be authenticated.")
	
	def getFavorites(self, page = "1"):
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/favorites.json?page=" + page))
			except HTTPError, e:
				raise TangoError("getFavorites() failed with a %s error code." % `e.code`, e.code)
		else:
			raise TangoError("getFavorites() requires you to be authenticated.")
	
	def createFavorite(self, id):
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/favorites/create/" + id + ".json", ""))
			except HTTPError, e:
				raise TangoError("createFavorite() failed with a %s error code." % `e.code`, e.code)
		else:
			raise TangoError("createFavorite() requires you to be authenticated.")
	
	def destroyFavorite(self, id):
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/favorites/destroy/" + id + ".json", ""))
			except HTTPError, e:
				raise TangoError("destroyFavorite() failed with a %s error code." %	`e.code`, e.code)
		else:
			raise TangoError("destroyFavorite() requires you to be authenticated.")
	
	def notificationFollow(self, id = None, user_id = None, screen_name = None):
		if self.authenticated is True:
			apiURL = ""
			if id is not None:
				apiURL = "http://twitter.com/notifications/follow/" + id + ".json"
			if user_id is not None:
				apiURL = "http://twitter.com/notifications/follow/follow.json?user_id=" + user_id
			if screen_name is not None:
				apiURL = "http://twitter.com/notifications/follow/follow.json?screen_name=" + screen_name
			try:
				return simplejson.load(self.opener.open(apiURL, ""))
			except HTTPError, e:
				raise TangoError("notificationFollow() failed with a %s error code." % `e.code`, e.code)
		else:
			raise TangoError("notificationFollow() requires you to be authenticated.")
	
	def notificationLeave(self, id = None, user_id = None, screen_name = None):
		if self.authenticated is True:
			apiURL = ""
			if id is not None:
				apiURL = "http://twitter.com/notifications/leave/" + id + ".json"
			if user_id is not None:
				apiURL = "http://twitter.com/notifications/leave/leave.json?user_id=" + user_id
			if screen_name is not None:
				apiURL = "http://twitter.com/notifications/leave/leave.json?screen_name=" + screen_name
			try:
				return simplejson.load(self.opener.open(apiURL, ""))
			except HTTPError, e:
				raise TangoError("notificationLeave() failed with a %s error code." % `e.code`, e.code)
		else:
			raise TangoError("notificationLeave() requires you to be authenticated.")
	
	def getFriendsIDs(self, id = None, user_id = None, screen_name = None, page = "1"):
		apiURL = ""
		if id is not None:
			apiURL = "http://twitter.com/friends/ids/" + id + ".json" + "?page=" + page
		if user_id is not None:
			apiURL = "http://twitter.com/friends/ids.json?user_id=" + user_id + "&page=" + page
		if screen_name is not None:
			apiURL = "http://twitter.com/friends/ids.json?screen_name=" + screen_name + "&page=" + page
		try:
			return simplejson.load(urllib2.urlopen(apiURL))
		except HTTPError, e:
			raise TangoError("getFriendsIDs() failed with a %s error code." % `e.code`, e.code)
		
	def getFollowersIDs(self, id = None, user_id = None, screen_name = None, page = "1"):
		apiURL = ""
		if id is not None:
			apiURL = "http://twitter.com/followers/ids/" + id + ".json" + "?page=" + page
		if user_id is not None:
			apiURL = "http://twitter.com/followers/ids.json?user_id=" + user_id + "&page=" + page
		if screen_name is not None:
			apiURL = "http://twitter.com/followers/ids.json?screen_name=" + screen_name + "&page=" + page
		try:
			return simplejson.load(urllib2.urlopen(apiURL))
		except HTTPError, e:
			raise TangoError("getFollowersIDs() failed with a %s error code." % `e.code`, e.code)
	
	def createBlock(self, id):
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/blocks/create/" + id + ".json", ""))
			except HTTPError, e:
				raise TangoError("createBlock() failed with a %s error code." % `e.code`, e.code)
		else:
			raise TangoError("createBlock() requires you to be authenticated.")
	
	def destroyBlock(self, id):
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/blocks/destroy/" + id + ".json", ""))
			except HTTPError, e:
				raise TangoError("destroyBlock() failed with a %s error code." % `e.code`, e.code)
		else:
			raise TangoError("destroyBlock() requires you to be authenticated.")
	
	def checkIfBlockExists(self, id = None, user_id = None, screen_name = None):
		apiURL = ""
		if id is not None:
			apiURL = "http://twitter.com/blocks/exists/" + id + ".json"
		if user_id is not None:
			apiURL = "http://twitter.com/blocks/exists.json?user_id=" + user_id
		if screen_name is not None:
			apiURL = "http://twitter.com/blocks/exists.json?screen_name=" + screen_name
		try:
			return simplejson.load(urllib2.urlopen(apiURL))
		except HTTPError, e:
			raise TangoError("checkIfBlockExists() failed with a %s error code." % `e.code`, e.code)
	
	def getBlocking(self, page = "1"):
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/blocks/blocking.json?page=" + page))
			except HTTPError, e:
				raise TangoError("getBlocking() failed with a %s error code." %	`e.code`, e.code)
		else:
			raise TangoError("getBlocking() requires you to be authenticated")
	
	def getBlockedIDs(self):
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/blocks/blocking/ids.json"))
			except HTTPError, e:
				raise TangoError("getBlockedIDs() failed with a %s error code." % `e.code`, e.code)
		else:
			raise TangoError("getBlockedIDs() requires you to be authenticated.")
	
	def searchTwitter(self, search_query, **kwargs):
		searchURL = self.constructApiURL("http://search.twitter.com/search.json", kwargs) + "&" + urllib.urlencode({"q": search_query})
		try:
			return simplejson.load(urllib2.urlopen(searchURL))
		except HTTPError, e:
			raise TangoError("getSearchTimeline() failed with a %s error code." % `e.code`, e.code)
	
	def getCurrentTrends(self, excludeHashTags = False):
		apiURL = "http://search.twitter.com/trends/current.json"
		if excludeHashTags is True:
			apiURL += "?exclude=hashtags"
		try:
			return simplejson.load(urllib.urlopen(apiURL))
		except HTTPError, e:
			raise TangoError("getCurrentTrends() failed with a %s error code." % `e.code`, e.code)
	
	def getDailyTrends(self, date = None, exclude = False):
		apiURL = "http://search.twitter.com/trends/daily.json"
		questionMarkUsed = False
		if date is not None:
			apiURL += "?date=" + date
			questionMarkUsed = True
		if exclude is True:
			if questionMarkUsed is True:
				apiURL += "&exclude=hashtags"
			else:
				apiURL += "?exclude=hashtags"
		try:
			return simplejson.load(urllib.urlopen(apiURL))
		except HTTPError, e:
			raise TangoError("getDailyTrends() failed with a %s error code." % `e.code`, e.code)
	
	def getWeeklyTrends(self, date = None, exclude = False):
		apiURL = "http://search.twitter.com/trends/daily.json"
		questionMarkUsed = False
		if date is not None:
			apiURL += "?date=" + date
			questionMarkUsed = True
		if exclude is True:
			if questionMarkUsed is True:
				apiURL += "&exclude=hashtags"
			else:
				apiURL += "?exclude=hashtags"
		try:
			return simplejson.load(urllib.urlopen(apiURL))
		except HTTPError, e:
			raise TangoError("getWeeklyTrends() failed with a %s error code." % `e.code`, e.code)
	
	def getSavedSearches(self):
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/saved_searches.json"))
			except HTTPError, e:
				raise TangoError("getSavedSearches() failed with a %s error code." % `e.code`, e.code)
		else:
			raise TangoError("getSavedSearches() requires you to be authenticated.")
	
	def showSavedSearch(self, id):
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/saved_searches/show/" + id + ".json"))
			except HTTPError, e:
				raise TangoError("showSavedSearch() failed with a %s error code." % `e.code`, e.code)
		else:
			raise TangoError("showSavedSearch() requires you to be authenticated.")
	
	def createSavedSearch(self, query):
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/saved_searches/create.json?query=" + query, ""))
			except HTTPError, e:
				raise TangoError("createSavedSearch() failed with a %s error code." % `e.code`, e.code)
		else:
			raise TangoError("createSavedSearch() requires you to be authenticated.")
	
	def destroySavedSearch(self, id):
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/saved_searches/destroy/" + id + ".json", ""))
			except HTTPError, e:
				raise TangoError("destroySavedSearch() failed with a %s error code." % `e.code`, e.code)
		else:
			raise TangoError("destroySavedSearch() requires you to be authenticated.")
	
	# The following methods are apart from the other Account methods, because they rely on a whole multipart-data posting function set.
	def updateProfileBackgroundImage(self, filename, tile="true"):
		if self.authenticated is True:
			try:
				files = [("image", filename, open(filename).read())]
				fields = []
				content_type, body = self.encode_multipart_formdata(fields, files)
				headers = {'Content-Type': content_type, 'Content-Length': str(len(body))}
				r = urllib2.Request("http://twitter.com/account/update_profile_background_image.json?tile=" + tile, body, headers)
				return self.opener.open(r).read()
			except HTTPError, e:
				raise TangoError("updateProfileBackgroundImage() failed with a %s error code." % `e.code`, e.code)
		else:
			raise TangoError("You realize you need to be authenticated to change a background image, right?")
	
	def updateProfileImage(self, filename):
		if self.authenticated is True:
			try:
				files = [("image", filename, open(filename).read())]
				fields = []
				content_type, body = self.encode_multipart_formdata(fields, files)
				headers = {'Content-Type': content_type, 'Content-Length': str(len(body))}
				r = urllib2.Request("http://twitter.com/account/update_profile_image.json", body, headers)
				return self.opener.open(r).read()
			except HTTPError, e:
				raise TangoError("updateProfileImage() failed with a %s error code." % `e.code`, e.code)
		else:
			raise TangoError("You realize you need to be authenticated to change a profile image, right?")
	
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
