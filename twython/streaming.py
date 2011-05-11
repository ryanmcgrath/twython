#!/usr/bin/python

"""
	TwythonStreamer is an implementation of the Streaming API for Twython.
	Pretty self explanatory by reading the code below. It's worth noting
	that the end user should, ideally, never import this library, but rather
	this is exposed via a linking method in Twython's core.

	Questions, comments? ryan@venodesigns.net
"""

__author__ = "Ryan McGrath <ryan@venodesigns.net>"
__version__ = "1.0.0"

import urllib
import urllib2
import urlparse
import httplib
import httplib2
import re

from urllib2 import HTTPError

# There are some special setups (like, oh, a Django application) where
# simplejson exists behind the scenes anyway. Past Python 2.6, this should
# never really cause any problems to begin with.
try:
	# Python 2.6 and up
	import json as simplejson
except ImportError:
	try:
		# Python 2.6 and below (2.4/2.5, 2.3 is not guranteed to work with this library to begin with)
		import simplejson
	except ImportError:
		try:
			# This case gets rarer by the day, but if we need to, we can pull it from Django provided it's there.
			from django.utils import simplejson
		except:
			# Seriously wtf is wrong with you if you get this Exception.
			raise Exception("Twython requires the simplejson library (or Python 2.6) to work. http://www.undefined.org/python/")

class TwythonStreamingError(Exception):
	def __init__(self, msg):
		self.msg = msg

	def __str__(self):
		return str(self.msg)

feeds = {
	"firehose": "http://stream.twitter.com/firehose.json",
	"gardenhose": "http://stream.twitter.com/gardenhose.json",
	"spritzer": "http://stream.twitter.com/spritzer.json",
	"birddog": "http://stream.twitter.com/birddog.json",
	"shadow": "http://stream.twitter.com/shadow.json",
	"follow": "http://stream.twitter.com/follow.json",
	"track": "http://stream.twitter.com/track.json",
}

class Stream(object):
	def __init__(self, username = None, password = None, feed = "spritzer", user_agent = "Twython Streaming"):
	  pass
