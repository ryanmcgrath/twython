from twython import Twython

""" Instantiate Twython with no Authentication """
twitter = Twython()
search_results = twitter.searchTwitter(q="WebsDotCom", rpp="50")

for tweet in search_results["results"]:
	print tweet["text"]
