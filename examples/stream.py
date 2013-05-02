from twython import TwythonStreamer, TwythonStreamHandler


class MyHandler(TwythonStreamHandler):
    def on_success(self, data):
        print data

    def on_error(self, status_code, data):
        print status_code, data

handler = MyHandler()

# Requires Authentication as of Twitter API v1.1
stream = TwythonStreamer(APP_KEY, APP_SECRET,
                         OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                         handler)

stream.statuses.filter(track='twitter')
#stream.user(track='twitter')
#stream.site(follow='twitter')
