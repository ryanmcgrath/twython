#!/usr/bin/python

"""
	Yes, this is just in __init__ for now, hush.

	The beginnings of Twitter Streaming API support in Twython. Don't expect this to work at all,
	consider it a stub for now. -- Ryan
	
	Questions, comments? ryan@venodesigns.net
"""

import httplib, urllib, urllib2, mimetypes, mimetools, socket, time

from urllib2 import HTTPError

try:
	import simplejson
except ImportError:
	try:
		import json as simplejson
	except ImportError:
		try:
			from django.utils import simplejson
		except:
			raise Exception("Twython (Streaming) requires the simplejson library (or Python 2.6) to work. http://www.undefined.org/python/")

__author__ = "Ryan McGrath <ryan@venodesigns.net>"
__version__ = "0.1"

class TwythonStreamingError(Exception):
	def __init__(self, msg):
		self.msg = msg
	def __str__(self):
		return repr(self.msg)

feeds = {
	"firehose": "http://stream.twitter.com/firehose.json",
	"gardenhose": "http://stream.twitter.com/gardenhose.json",
	"spritzer": "http://stream.twitter.com/spritzer.json",
	"birddog": "http://stream.twitter.com/birddog.json",
	"shadow": "http://stream.twitter.com/shadow.json",
	"follow": "http://stream.twitter.com/follow.json",
	"track": "http://stream.twitter.com/track.json",
}

class stream:
	def __init__(self, username = None, password = None, feed = "spritzer", user_agent = "Twython Streaming"):
		self.username = username
		self.password = password
		self.feed = feeds[feed]
		self.user_agent = user_agent
		self.connection_open = False
