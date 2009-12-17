#!/usr/bin/python

"""
	Twython-oauth (twyauth) is a separate library to handle OAuth routines with Twython. This currently doesn't work, as I never get the time to finish it.
	Feel free to help out.

	Questions, comments? ryan@venodesigns.net
"""

import httplib, urllib, urllib2, mimetypes, mimetools

from urlparse import urlparse
from urllib2 import HTTPError

try:
	import oauth
except ImportError:
	pass

class oauth:
	def __init__(self, username, consumer_key, consumer_secret, signature_method = None, headers = None, version = 1):
		"""oauth(username = None, consumer_secret = None, consumer_key = None, headers = None)

			Instantiates an instance of Twython with OAuth. Takes optional parameters for authentication and such (see below).

			Parameters:
				username - Your Twitter username, if you want Basic (HTTP) Authentication.
				consumer_secret - Consumer secret, given to you when you register your App with Twitter.
				consumer_key - Consumer key (see situation with consumer_secret).
				signature_method - Method for signing OAuth requests; defaults to oauth.OAuthSignatureMethod_HMAC_SHA1()
				headers - User agent header.
				version (number) - Twitter supports a "versioned" API as of Oct. 16th, 2009 - this defaults to 1, but can be overridden on a class and function-based basis.
		"""
		# OAuth specific variables below
		self.request_token_url = 'https://api.twitter.com/%s/oauth/request_token' % version
		self.access_token_url = 'https://api.twitter.com/%s/oauth/access_token' % version
		self.authorization_url = 'http://api.twitter.com/%s/oauth/authorize' % version
		self.signin_url = 'http://api.twitter.com/%s/oauth/authenticate' % version
		self.consumer_key = consumer_key
		self.consumer_secret = consumer_secret
		self.request_token = None
		self.access_token = None
		self.consumer = None
		self.connection = None
		self.signature_method = None
		self.consumer = oauth.OAuthConsumer(self.consumer_key, self.consumer_secret)
		self.connection = httplib.HTTPSConnection("http://api.twitter.com")
	
	def getOAuthResource(self, url, access_token, params, http_method="GET"):
		"""getOAuthResource(self, url, access_token, params, http_method="GET")

			Returns a signed OAuth object for use in requests.
		"""
		newRequest = oauth.OAuthRequest.from_consumer_and_token(consumer, token=self.access_token, http_method=http_method, http_url=url, parameters=parameters)
		oauth_request.sign_request(self.signature_method, consumer, access_token)
		return oauth_request
	
	def getResponse(self, oauth_request, connection):
		"""getResponse(self, oauth_request, connection)

			Returns a JSON-ified list of results.
		"""
		url = oauth_request.to_url()
		connection.request(oauth_request.http_method, url)
		response = connection.getresponse()
		return simplejson.load(response.read())
	
	def getUnauthorisedRequestToken(self, consumer, connection, signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()):
		oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer, consumer, http_url=self.request_token_url)
		oauth_request.sign_request(signature_method, consumer, None)
		resp = fetch_response(oauth_request, connection)
		return oauth.OAuthToken.from_string(resp)
	
	def getAuthorizationURL(self, consumer, token, signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()):
		oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer, token=token, http_url=self.authorization_url)
		oauth_request.sign_request(signature_method, consumer, token)
		return oauth_request.to_url()
	
	def exchangeRequestTokenForAccessToken(self, consumer, connection, request_token, signature_method = oauth.OAuthSignatureMethod_HMAC_SHA1()):
		# May not be needed...
		self.request_token = request_token
		oauth_request = oauth.OAuthRequest.from_consumer_and_token(consumer, token = request_token, http_url=self.access_token_url)
		oauth_request.sign_request(signature_method, consumer, request_token)
		resp = fetch_response(oauth_request, connection)
		return oauth.OAuthToken.from_string(resp)
