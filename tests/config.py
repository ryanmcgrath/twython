# -*- coding: utf-8 -*-
import os

import sys
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

