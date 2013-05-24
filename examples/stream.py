from twython import TwythonStreamer


class MyStreamer(TwythonStreamer):
    def on_success(self, data):
        print data
        # Want to disconnect after the first result?
        # self.disconnect()

    def on_error(self, status_code, data):
        print status_code, data

# Requires Authentication as of Twitter API v1.1
stream = MyStreamer(APP_KEY, APP_SECRET,
                    OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

stream.statuses.filter(track='twitter')
#stream.user(track='twitter')
#stream.site(follow='twitter')
