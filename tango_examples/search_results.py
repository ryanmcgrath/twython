import tango

""" Instantiate Tango with no Authentication """
twitter = tango.setup()
search_results = twitter.searchTwitter("WebsDotCom", rpp="50")

for tweet in search_results["results"]:
	print tweet["text"]
