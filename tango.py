#!/usr/bin/python

"""
	Tango is an up-to-date library for Python that wraps the Twitter API.
	Other Python Twitter libraries seem to have fallen a bit behind, and
	Twitter's API has evolved a bit. Here's hoping this helps.

	TODO: OAuth, Streaming API?

	Questions, comments? ryan@venodesigns.net
"""

import httplib, urllib, urllib2, mimetypes, mimetools

from urllib2 import HTTPError

try:
	import simplejson
except ImportError:
	print "Tango requires the simplejson library to work. http://www.undefined.org/python/"

try:
	import oauth
except ImportError:
	print "Tango requires oauth for authentication purposes. http://oauth.googlecode.com/svn/code/python/oauth/oauth.py"

class setup:
	def __init__(self, authtype = "OAuth", username = None, password = None, oauth_keys = None, debug = False):
		self.authtype = authtype
		self.authenticated = False
		self.username = username
		self.password = password
		self.oauth_keys = oauth_keys
		self.debug = debug
		if self.username is not None and self.password is not None:
			if self.authtype == "OAuth":
				pass
			elif self.authtype == "Basic":
				self.auth_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
				self.auth_manager.add_password(None, "http://twitter.com", self.username, self.password)
				self.handler = urllib2.HTTPBasicAuthHandler(self.auth_manager)
				self.opener = urllib2.build_opener(self.handler)
				self.authenticated = True
	
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
			if self.debug is True:
				print e.headers
			print "shortenURL() failed with a " + str(e.code) + " error code."
	
	def constructApiURL(self, base_url, params, **kwargs):
		queryURL = base_url
		questionMarkUsed = False
		if kwargs.has_key("questionMarkUsed") is True:
			questionMarkUsed = True
		for param in params:
			if params[param] is not None:
				queryURL += (("&" if questionMarkUsed is True else "?") + param + "=" + params[param])
				questionMarkUsed = True
		return queryURL
	
	def getRateLimitStatus(self, rate_for = "requestingIP"):
		try:
			if rate_for == "requestingIP":
				return simplejson.load(urllib2.urlopen("http://twitter.com/account/rate_limit_status.json"))
			else:
				return simplejson.load(self.opener.open("http://twitter.com/account/rate_limit_status.json"))
		except HTTPError, e:
			if self.debug is True:
				print e.headers
			print "It seems that there's something wrong. Twitter gave you a " + str(e.code) + " error code; are you doing something you shouldn't be?"
	
	def getPublicTimeline(self):
		try:
			return simplejson.load(urllib2.urlopen("http://twitter.com/statuses/public_timeline.json"))
		except HTTPError, e:
			if self.debug is True:
				print e.headers
			print "getPublicTimeline() failed with a " + str(e.code) + " error code."
	
	def getFriendsTimeline(self, **kwargs):
		if self.authenticated is True:
			try:
				friendsTimelineURL = self.constructApiURL("http://twitter.com/statuses/friends_timeline.json", kwargs)
				return simplejson.load(self.opener.open(friendsTimelineURL))
			except HTTPError, e:
				if self.debug is True:
					print e.headers
				print "getFriendsTimeline() failed with a " + str(e.code) + " error code."
		else:
			print "getFriendsTimeline() requires you to be authenticated."
	
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
			if self.debug is True:
				print e.headers
			print "Failed with a " + str(e.code) + " error code. Does this user hide/protect their updates? If so, you'll need to authenticate and be their friend to get their timeline."
	
	def getUserMentions(self, **kwargs):
		if self.authenticated is True:
			try:
				mentionsFeedURL = self.constructApiURL("http://twitter.com/statuses/mentions.json", kwargs)
				return simplejson.load(self.opener.open(mentionsFeedURL))
			except HTTPError, e:
				if self.debug is True:
					print e.headers
				print "getUserMentions() failed with a " + str(e.code) + " error code."
		else:
			print "getUserMentions() requires you to be authenticated."
	
	def showStatus(self, id):
		try:
			return simplejson.load(self.opener.open("http://twitter.com/statuses/show/" + id + ".json"))
		except HTTPError, e:
			if self.debug is True:
				print e.headers
			print "Failed with a " + str(e.code) + " error code. Does this user hide/protect their updates? If so, you'll need to authenticate and be their friend to get their timeline."

	def updateStatus(self, status, in_reply_to_status_id = None):
		if len(list(status)) > 140:
			print "This status message is over 140 characters, but we're gonna try it anyway. Might wanna watch this!"
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/statuses/update.json?", urllib.urlencode({"status": status}, {"in_reply_to_status_id": in_reply_to_status_id})))
			except HTTPError, e:
				if self.debug is True:
					print e.headers
				print "updateStatus() failed with a " + str(e.code) + " error code."
		else:
			print "updateStatus() requires you to be authenticated."
	
	def destroyStatus(self, id):
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/status/destroy/" + id + ".json", "POST"))
			except HTTPError, e:
				if self.debug is True:
					print e.headers
				print "destroyStatus() failed with a " + str(e.code) + " error code."
		else:
			print "destroyStatus() requires you to be authenticated."
	
	def endSession(self):
		if self.authenticated is True:
			try:
				self.opener.open("http://twitter.com/account/end_session.json", "")
				self.authenticated = False
			except HTTPError, e:
				if self.debug is True:
					print e.headers
				print "endSession failed with a " + str(e.code) + " error code."
		else:
			print "You can't end a session when you're not authenticated to begin with."
	
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
				if self.debug is True:
					print e.headers
				print "getDirectMessages() failed with a " + str(e.code) + " error code."
		else:
			print "getDirectMessages() requires you to be authenticated."
	
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
				if self.debug is True:
					print e.headers
				print "getSentMessages() failed with a " + str(e.code) + " error code."
		else:
			print "getSentMessages() requires you to be authenticated."
	
	def sendDirectMessage(self, user, text):
		if self.authenticated is True:
			if len(list(text)) < 140:
				try:
					return self.opener.open("http://twitter.com/direct_messages/new.json", urllib.urlencode({"user": user, "text": text}))
				except HTTPError, e:
					if self.debug is True:
						print e.headers
					print "sendDirectMessage() failed with a " + str(e.code) + " error code."
			else:
				print "Your message must be longer than 140 characters"
		else:
			print "You must be authenticated to send a new direct message."
	
	def destroyDirectMessage(self, id):
		if self.authenticated is True:
			try:
				return self.opener.open("http://twitter.com/direct_messages/destroy/" + id + ".json", "")
			except HTTPError, e:
				if self.debug is True:
					print e.headers
				print "destroyDirectMessage() failed with a " + str(e.code) + " error code."
		else:
			print "You must be authenticated to destroy a direct message."
	
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
				if self.debug is True:
					print e.headers
				print "createFriendship() failed with a " + str(e.code) + " error code. "
				if e.code == 403:
					print "It seems you've hit the update limit for this method. Try again in 24 hours."
		else:
			print "createFriendship() requires you to be authenticated."
		
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
				if self.debug is True:
					print e.headers
				print "destroyFriendship() failed with a " + str(e.code) + " error code."
		else:
			print "destroyFriendship() requires you to be authenticated."
	
	def checkIfFriendshipExists(self, user_a, user_b):
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/friendships/exists.json", urllib.urlencode({"user_a": user_a, "user_b": user_b})))
			except HTTPError, e:
				if self.debug is True:
					print e.headers
				print "checkIfFriendshipExists() failed with a " + str(e.code) + " error code."
		else:
			print "checkIfFriendshipExists(), oddly, requires that you be authenticated."
	
	def updateDeliveryDevice(self, device_name = "none"):
		if self.authenticated is True:
			try:
				return self.opener.open("http://twitter.com/account/update_delivery_device.json?", urllib.urlencode({"device": device_name}))
			except HTTPError, e:
				if self.debug is True:
					print e.headers
				print "updateDeliveryDevice() failed with a " + str(e.code) + " error code."
		else:
			print "updateDeliveryDevice() requires you to be authenticated."
	
	def updateProfileColors(self, **kwargs):
		if self.authenticated is True:
			try:
				return self.opener.open(self.constructApiURL("http://twitter.com/account/update_profile_colors.json?", kwargs))
			except HTTPError, e:
				if self.debug is True:
					print e.headers
				print "updateProfileColors() failed with a " + str(e.code) + " error code."
		else:
			print "updateProfileColors() requires you to be authenticated."
	
	def updateProfile(self, name = None, email = None, url = None, location = None, description = None):
		if self.authenticated is True:
			useAmpersands = False
			updateProfileQueryString = ""
			if name is not None:
				if len(list(name)) < 20:
					updateProfileQueryString += "name=" + name
					useAmpersands = True
				else:
					print "Twitter has a character limit of 20 for all usernames. Try again."
			if email is not None and "@" in email:
				if len(list(email)) < 40:
					if useAmpersands is True:
						updateProfileQueryString += "&email=" + email
					else:
						updateProfileQueryString += "email=" + email
						useAmpersands = True
				else:
					print "Twitter has a character limit of 40 for all email addresses, and the email address must be valid. Try again."
			if url is not None:
				if len(list(url)) < 100:
					if useAmpersands is True:
						updateProfileQueryString += "&" + urllib.urlencode({"url": url})
					else:
						updateProfileQueryString += urllib.urlencode({"url": url})
						useAmpersands = True
				else:
					print "Twitter has a character limit of 100 for all urls. Try again."
			if location is not None:
				if len(list(location)) < 30:
					if useAmpersands is True:
						updateProfileQueryString += "&" + urllib.urlencode({"location": location})
					else:
						updateProfileQueryString += urllib.urlencode({"location": location})
						useAmpersands = True
				else:
					print "Twitter has a character limit of 30 for all locations. Try again."
			if description is not None:
				if len(list(description)) < 160:
					if useAmpersands is True:
						updateProfileQueryString += "&" + urllib.urlencode({"description": description})
					else:
						updateProfileQueryString += urllib.urlencode({"description": description})
				else:
					print "Twitter has a character limit of 160 for all descriptions. Try again."
			
			if updateProfileQueryString != "":
				try:
					return self.opener.open("http://twitter.com/account/update_profile.json?", updateProfileQueryString)
				except HTTPError, e:
					if self.debug is True:
						print e.headers
					print "updateProfile() failed with a " + e.code + " error code."
		else:
			# If they're not authenticated
			print "updateProfile() requires you to be authenticated."
	
	def getFavorites(self, page = "1"):
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/favorites.json?page=" + page))
			except HTTPError, e:
				if self.debug:
					print e.headers
				print "getFavorites() failed with a " + str(e.code) + " error code."
		else:
			print "getFavorites() requires you to be authenticated."
	
	def createFavorite(self, id):
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/favorites/create/" + id + ".json", ""))
			except HTTPError, e:
				if self.debug:
					print e.headers
				print "createFavorite() failed with a " + str(e.code) + " error code."
		else:
			print "createFavorite() requires you to be authenticated."
	
	def destroyFavorite(self, id):
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/favorites/destroy/" + id + ".json", ""))
			except HTTPError, e:
				if self.debug:
					print e.headers
				print "destroyFavorite() failed with a " + str(e.code) + " error code."
		else:
			print "destroyFavorite() requires you to be authenticated."
	
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
				if self.debug is True:
					print e.headers
				print "notificationFollow() failed with a " + str(e.code) + " error code."
		else:
			print "notificationFollow() requires you to be authenticated."
	
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
				if self.debug is True:
					print e.headers
				print "notificationLeave() failed with a " + str(e.code) + " error code."
		else:
			print "notificationLeave() requires you to be authenticated."
	
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
			if self.debug is True:
				print e.headers
			print "getFriendsIDs() failed with a " + str(e.code) + " error code."
		
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
			if self.debug is True:
				print e.headers
			print "getFollowersIDs() failed with a " + str(e.code) + " error code."
	
	def createBlock(self, id):
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/blocks/create/" + id + ".json", ""))
			except HTTPError, e:
				if self.debug is True:
					print e.headers
				print "createBlock() failed with a " + str(e.code) + " error code."
		else:
			print "createBlock() requires you to be authenticated."
	
	def destroyBlock(self, id):
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/blocks/destroy/" + id + ".json", ""))
			except HTTPError, e:
				if self.debug is True:
					print e.headers
				print "destroyBlock() failed with a " + str(e.code) + " error code."
		else:
			print "destroyBlock() requires you to be authenticated."
	
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
			if self.debug is True:
				print e.headers
			print "checkIfBlockExists() failed with a " + str(e.code) + " error code."
	
	def getBlocking(self, page = "1"):
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/blocks/blocking.json?page=" + page))
			except HTTPError, e:
				if self.debug is True:
					print e.headers
				print "getBlocking() failed with a " + str(e.code) + " error code."
		else:
			print "getBlocking() requires you to be authenticated"
	
	def getBlockedIDs(self):
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/blocks/blocking/ids.json"))
			except HTTPError, e:
				if self.debug is True:
					print e.headers
				print "getBlockedIDs() failed with a " + str(e.code) + " error code."
		else:
			print "getBlockedIDs() requires you to be authenticated."
	
	def searchTwitter(self, search_query, **kwargs):
		baseURL = "http://search.twitter.com/search.json?" + urllib.urlencode({"q": search_query})
		searchURL = self.constructApiURL(baseURL, kwargs, questionMarkUsed=True)
		try:
			return simplejson.load(urllib2.urlopen(searchURL))
		except HTTPError, e:
			if self.debug is True:
				print e.headers
			print "getSearchTimeline() failed with a " + str(e.code) + " error code."
	
	def getCurrentTrends(self, excludeHashTags = False):
		apiURL = "http://search.twitter.com/trends/current.json"
		if excludeHashTags is True:
			apiURL += "?exclude=hashtags"
		try:
			return simplejson.load(urllib.urlopen(apiURL))
		except HTTPError, e:
			if self.debug is True:
				print e.headers
			print "getCurrentTrends() failed with a " + str(e.code) + " error code."
	
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
			if self.debug is True:
				print e.headers
			print "getDailyTrends() failed with a " + str(e.code) + " error code."
	
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
			if self.debug is True:
				print e.headers
			print "getWeeklyTrends() failed with a " + str(e.code) + " error code."
	
	def getSavedSearches(self):
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/saved_searches.json"))
			except HTTPError, e:
				if self.debug is True:
					print e.headers
				print "getSavedSearches() failed with a " + str(e.code) + " error code."
		else:
			print "getSavedSearches() requires you to be authenticated."
	
	def showSavedSearch(self, id):
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/saved_searches/show/" + id + ".json"))
			except HTTPError, e:
				if self.debug is True:
					print e.headers
				print "showSavedSearch() failed with a " + str(e.code) + " error code."
		else:
			print "showSavedSearch() requires you to be authenticated."
	
	def createSavedSearch(self, query):
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/saved_searches/create.json?query=" + query, ""))
			except HTTPError, e:
				if self.debug is True:
					print e.headers
				print "createSavedSearch() failed with a " + str(e.code) + " error code."
		else:
			print "createSavedSearch() requires you to be authenticated."
	
	def destroySavedSearch(self, id):
		if self.authenticated is True:
			try:
				return simplejson.load(self.opener.open("http://twitter.com/saved_searches/destroy/" + id + ".json", ""))
			except HTTPError, e:
				if self.debug is True:
					print e.headers
				print "destroySavedSearch() failed with a " + str(e.code) + " error code."
		else:
			print "destroySavedSearch() requires you to be authenticated."
	
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
				if self.debug is True:
					print e.headers
				print "updateProfileBackgroundImage() failed with a " + str(e.code) + " error code."
		else:
			print "You realize you need to be authenticated to change a background image, right?"
	
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
				if self.debug is True:
					print e.headers
				print "updateProfileImage() failed with a " + str(e.code) + " error code."
		else:
			print "You realize you need to be authenticated to change a profile image, right?"
	
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
