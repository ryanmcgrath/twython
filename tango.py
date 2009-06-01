#!/usr/bin/python

"""
	Tango is an up-to-date library for Python that wraps the Twitter API.
	Other Python Twitter libraries seem to have fallen a bit behind, and
	Twitter's API has evolved a bit. Here's hoping this helps.

	Questions, comments? ryan@venodesigns.net
"""

import httplib, urllib, urllib2, mimetypes

from urllib2 import HTTPError

try:
	import simplejson
except:
	print "Tango requires the simplejson library to work. http://www.undefined.org/python/"

try:
	import oauth
except:
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
		else:
			pass
	
	def explainOAuthSupport(self):
		print "Sorry, OAuth support is still forthcoming. Default back to Basic Authentication for now, or help out on this front!"
		pass

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
		shortURL = urllib2.urlopen(shortener + "?" + urllib.urlencode({query: url_to_shorten})).read()
		return shortURL
	
	def constructApiURL(self, base_url, params):
		queryURL = base_url
		questionMarkUsed = False
		for param in params:
			if params[param] is not None:
				queryURL += (("&" if questionMarkUsed is True else "?") + param + "=" + params[param])
				questionMarkUsed = True
		return queryURL
	
	def createGenericTimeline(self, existingTimeline):
		# Many of Twitter's API functions return the same style of data. This function just wraps it if we need it.
		genericTimeline = []
		for tweet in existingTimeline:
			genericTimeline.append({
				"created_at": tweet["created_at"],
				"in_reply_to_screen_name": tweet["in_reply_to_screen_name"],
				"in_reply_to_status_id": tweet["in_reply_to_status_id"],
				"in_reply_to_user_id": tweet["in_reply_to_user_id"],
				"id": tweet["id"], 
				"text": tweet["text"]
			})
		return genericTimeline
	
	def getRateLimitStatus(self, rate_for = "requestingIP"):
		try:
			if rate_for == "requestingIP":
				rate_limit = simplejson.load(urllib2.urlopen("http://twitter.com/account/rate_limit_status.json"))
			else:
				rate_limit = simplejson.load(self.opener.open("http://twitter.com/account/rate_limit_status.json"))
		except HTTPError, e:
			if self.debug is True:
				print e.headers
			print "It seems that there's something wrong. Twitter gave you a " + e.code + " error code; are you doing something you shouldn't be?"
		return {"remaining-hits": rate_limit["remaining-hits"], 
				"hourly-limit": rate_limit["hourly-limit"], 
				"reset-time": rate_limit["reset-time"],
				"reset-time-in-seconds": rate_limit["reset-time-in-seconds"]}

	def getPublicTimeline(self):
		return self.createGenericTimeline(simplejson.load(urllib2.urlopen("http://twitter.com/statuses/public_timeline.json")))
	
	def getFriendsTimeline(self, **kwargs):
		if self.authenticated is True:
			friendsTimelineURL = self.constructApiURL("http://twitter.com/statuses/friends_timeline.json", kwargs)
			return self.createGenericTimeline(simplejson.load(self.opener.open(friendsTimelineURL)))
		else:
			print "getFriendsTimeline() requires you to be authenticated."
			pass
	
	def getUserTimeline(self, **kwargs): 
		userTimelineURL = self.constructApiURL("http://twitter.com/statuses/user_timeline/" + self.username + ".json", kwargs)
		try:
			return self.createGenericTimeline(simplejson.load(urllib2.urlopen(userTimelineURL)))
		except HTTPError, e:
			if self.debug is True:
				print e.headers
			print "Hmmm, failed with a " + e.code + " error code. Does this user hide/protect their updates? If so, you'll need to authenticate and be their friend to get their timeline."
			pass
	
	def getUserMentions(self, **kwargs):
		if self.authenticated is True:
			if self.authtype == "Basic":
				mentionsFeedURL = self.constructApiURL("http://twitter.com/statuses/mentions.json", kwargs)
				mentionsFeed = simplejson.load(self.opener.open(mentionsFeedURL))
				return self.createGenericTimeline(mentionsFeed)
			else:
				pass
		else:
			print "getUserMentions() requires you to be authenticated."
			pass
	
	def showStatus(self, id):
		try:
			tweet = simplejson.load(self.opener.open("http://twitter.com/statuses/show/" + id + ".json"))
			return {"created_at": tweet["created_at"], 
					"id": tweet["id"], 
					"text": tweet["text"], 
					"in_reply_to_status_id": tweet["in_reply_to_status_id"],
					"in_reply_to_user_id": tweet["in_reply_to_user_id"],
					"in_reply_to_screen_name": tweet["in_reply_to_screen_name"]}
		except HTTPError, e:
			if self.debug is True:
				print e.headers
			print "Hmmm, failed with a " + e.code + " error code. Does this user hide/protect their updates? If so, you'll need to authenticate and be their friend to get their timeline."
			pass

	def updateStatus(self, status, in_reply_to_status_id = None):
		if self.authenticated is True:
			if self.authtype == "Basic":
				try:
					self.opener.open("http://twitter.com/statuses/update.json?", urllib.urlencode({"status": status}, {"in_reply_to_status_id": in_reply_to_status_id}))
				except HTTPError, e:
					print e.code
					print e.headers
			else:
				self.explainOAuthSupport()
		else:
			print "updateStatus() requires you to be authenticated."
			pass
	
	def destroyStatus(self, id):
		if self.authenticated is True:
			if self.authtype == "Basic":
				self.opener.open("http://twitter.com/status/destroy/" + id + ".json", "POST")
			else:
				self.explainOAuthSupport()
		else:
			print "destroyStatus() requires you to be authenticated."
			pass
	
	def endSession(self):
		if self.authenticated is True:
			try:
				self.opener.open("http://twitter.com/account/end_session.json", "")
				self.authenticated = False
			except HTTPError, e:
				if self.debug is True:
					print e.headers
				print "endSession failed with a " + e.code + " error code."
				pass
		else:
			print "You can't end a session when you're not authenticated to begin with."
			pass
	
	def updateDeliveryDevice(self, device_name = "none"):
		if self.authenticated is True:
			try:
				self.opener.open("http://twitter.com/account/update_delivery_device.json?", urllib.urlencode({"device": device_name}))
			except HTTPError, e:
				if self.debug is True:
					print e.headers
				print "updateDeliveryDevice() failed with a " + e.code + " error code."
		else:
			print "updateDeliveryDevice() requires you to be authenticated."
	
	def updateProfileColors(self, **kwargs):
		if self.authenticated is True:
			try:
				self.opener.open(self.constructApiURL("http://twitter.com/account/update_profile_colors.json?", kwargs))
			except HTTPError, e:
				if self.debug is True:
					print e.headers
				print "updateProfileColors() failed with a " + e.code + " error code."
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
					self.opener.open("http://twitter.com/account/update_profile.json?", updateProfileQueryString)
				except HTTPError, e:
					if self.debug is True:
						print e.headers
					print "updateProfile() failed with a " + e.code + " error code."
		else:
			# If they're not authenticated
			print "updateProfile() requires you to be authenticated."
	
	def getSearchTimeline(self, search_query, optional_page):
		params = urllib.urlencode({'q': search_query, 'rpp': optional_page}) # Doesn't hurt to do pages this way. *shrug*
		try:
			searchTimeline = simplejson.load(urllib2.urlopen("http://search.twitter.com/search.json", params))
			# This one is custom built because the search feed is a bit different than the other feeds.
			genericTimeline = []
			for tweet in searchTimeline["results"]:
				genericTimeline.append({
					"created_at": tweet["created_at"],
					"from_user": tweet["from_user"],
					"from_user_id": tweet["from_user_id"],
					"profile_image_url": tweet["profile_image_url"],
					"id": tweet["id"],
					"text": tweet["text"],
					"to_user_id": tweet["to_user_id"]
				})
			return genericTimeline
		except HTTPError, e:
			print e.code
			print e.headers
	
	def getCurrentTrends(self):
		# Returns an array of dictionary items containing the current trends
		trendingTopicsURL = "http://search.twitter.com/trends.json"
		trendingTopics = simplejson.load(urllib.urlopen(trendingTopicsURL))
		trendingTopicsArray = []
		for topic in trendingTopics['trends']:
			trendingTopicsArray.append({"name" : topic['name'], "url" : topic['url']})
		return trendingTopicsArray
