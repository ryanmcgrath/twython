import os

import sys
if sys.version_info[0] == 2 and sys.version_info[1] == 6:
    import unittest2 as unittest
else:
    import unittest

app_key = os.environ.get('APP_KEY')
app_secret = os.environ.get('APP_SECRET')
oauth_token = os.environ.get('OAUTH_TOKEN')
oauth_token_secret = os.environ.get('OAUTH_TOKEN_SECRET')
access_token = os.environ.get('ACCESS_TOKEN')

screen_name = os.environ.get('SCREEN_NAME', '__twython__')

# Protected Account you ARE following and they ARE following you
protected_twitter_1 = os.environ.get('PROTECTED_TWITTER_1', 'TwythonSecure1')

# Protected Account you ARE NOT following
protected_twitter_2 = os.environ.get('PROTECTED_TWITTER_2', 'TwythonSecure2')

# Test Ids
test_tweet_id = os.environ.get('TEST_TWEET_ID', '318577428610031617')
test_list_slug = os.environ.get('TEST_LIST_SLUG', 'team')
test_list_owner_screen_name = os.environ.get('TEST_LIST_OWNER_SCREEN_NAME',
                                             'twitterapi')

test_tweet_object = {u'contributors': None, u'truncated': False, u'text': u'http://t.co/FCmXyI6VHd is a #cool site, lol! @mikehelmick shd #checkitout. Love, @__twython__ https://t.co/67pwRvY6z9 http://t.co/N6InAO4B71', u'in_reply_to_status_id': None, u'id': 349683012054683648, u'favorite_count': 0, u'source': u'web', u'retweeted': False, u'coordinates': None, u'entities': {u'symbols': [], u'user_mentions': [{u'id': 29251354, u'indices': [45, 57], u'id_str': u'29251354', u'screen_name': u'mikehelmick', u'name': u'Mike Helmick'}, {u'id': 1431865928, u'indices': [81, 93], u'id_str': u'1431865928', u'screen_name': u'__twython__', u'name': u'Twython'}], u'hashtags': [{u'indices': [28, 33], u'text': u'cool'}, {u'indices': [62, 73], u'text': u'checkitout'}], u'urls': [{u'url': u'http://t.co/FCmXyI6VHd', u'indices': [0, 22], u'expanded_url': u'http://google.com', u'display_url': u'google.com'}, {u'url': u'https://t.co/67pwRvY6z9', u'indices': [94, 117], u'expanded_url': u'https://github.com', u'display_url': u'github.com'}], u'media': [{u'id': 537884378513162240, u'id_str': u'537884378513162240', u'indices': [118, 140], u'media_url': u'http://pbs.twimg.com/media/B3by_g-CQAAhrO5.jpg', u'media_url_https': u'https://pbs.twimg.com/media/B3by_g-CQAAhrO5.jpg', u'url': u'http://t.co/N6InAO4B71', u'display_url': u'pic.twitter.com/N6InAO4B71', u'expanded_url': u'http://twitter.com/pingofglitch/status/537884380060844032/photo/1', u'type': u'photo', u'sizes': {u'large': {u'w': 1024, u'h': 640, u'resize': u'fit'}, u'thumb': {u'w': 150, u'h': 150, u'resize': u'crop'}, u'medium': {u'w': 600, u'h': 375, u'resize': u'fit'}, u'small': {u'w': 340, u'h': 212, u'resize': u'fit'}}}]}, u'in_reply_to_screen_name': None, u'id_str': u'349683012054683648', u'retweet_count': 0, u'in_reply_to_user_id': None, u'favorited': False, u'user': {u'follow_request_sent': False, u'profile_use_background_image': True, u'default_profile_image': True, u'id': 1431865928, u'verified': False, u'profile_text_color': u'333333', u'profile_image_url_https': u'https://si0.twimg.com/sticky/default_profile_images/default_profile_3_normal.png', u'profile_sidebar_fill_color': u'DDEEF6', u'entities': {u'description': {u'urls': []}}, u'followers_count': 1, u'profile_sidebar_border_color': u'C0DEED', u'id_str': u'1431865928', u'profile_background_color': u'3D3D3D', u'listed_count': 0, u'profile_background_image_url_https': u'https://si0.twimg.com/images/themes/theme1/bg.png', u'utc_offset': None, u'statuses_count': 2, u'description': u'', u'friends_count': 1, u'location': u'', u'profile_link_color': u'0084B4', u'profile_image_url': u'http://a0.twimg.com/sticky/default_profile_images/default_profile_3_normal.png', u'following': False, u'geo_enabled': False, u'profile_background_image_url': u'http://a0.twimg.com/images/themes/theme1/bg.png', u'screen_name': u'__twython__', u'lang': u'en', u'profile_background_tile': False, u'favourites_count': 0, u'name': u'Twython', u'notifications': False, u'url': None, u'created_at': u'Thu May 16 01:11:09 +0000 2013', u'contributors_enabled': False, u'time_zone': None, u'protected': False, u'default_profile': False, u'is_translator': False}, u'geo': None, u'in_reply_to_user_id_str': None, u'possibly_sensitive': False, u'lang': u'en', u'created_at': u'Wed Jun 26 00:18:21 +0000 2013', u'in_reply_to_status_id_str': None, u'place': None}
test_tweet_html = '<a href="http://t.co/FCmXyI6VHd" class="twython-url">google.com</a> is a <a href="https://twitter.com/search?q=%23cool" class="twython-hashtag">#cool</a> site, lol! <a href="https://twitter.com/mikehelmick" class="twython-mention">@mikehelmick</a> shd <a href="https://twitter.com/search?q=%23checkitout" class="twython-hashtag">#checkitout</a>. Love, <a href="https://twitter.com/__twython__" class="twython-mention">@__twython__</a> <a href="https://t.co/67pwRvY6z9" class="twython-url">github.com</a> <a href="http://t.co/N6InAO4B71" class="twython-media">pic.twitter.com/N6InAO4B71</a>'
