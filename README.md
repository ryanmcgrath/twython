# Twython

<a href="https://pypi.python.org/pypi/twython"><img src="https://img.shields.io/pypi/v/twython.svg?style=flat-square"></a>
<a href="https://pypi.python.org/pypi/twython"><img src="https://img.shields.io/pypi/dw/twython.svg?style=flat-square"></a>
<a href="https://travis-ci.org/ryanmcgrath/twython"><img src="https://img.shields.io/travis/ryanmcgrath/twython.svg?style=flat-square"></a>
<a href="https://coveralls.io/r/ryanmcgrath/twython?branch=master"><img src="https://img.shields.io/coveralls/ryanmcgrath/twython/master.svg?style=flat-square"></a>

`Twython` is a Python library providing an easy way to access Twitter data. Supports Python 3. It's been battle tested by companies, educational institutions and individuals alike. Try it today!

**Note**: As of Twython 3.7.0, there's a general call for maintainers put out. If you find the project useful and want to help out, reach out to Ryan with the info from the bottom of this README. Great open source project to get your feet wet with!

## Features
- Query data for:
    - User information
    - Twitter lists
    - Timelines
    - Direct Messages
    - and anything found in [the docs](https://developer.twitter.com/en/docs)
- Image Uploading:
    - Update user status with an image
    - Change user avatar
    - Change user background image
    - Change user banner image
- OAuth 2 Application Only (read-only) Support
- Support for Twitter's Streaming API
- Seamless Python 3 support!

## Installation
Install Twython via pip:

```bash
$ pip install twython
```

Or, if you want the code that is currently on GitHub

```bash
git clone git://github.com/ryanmcgrath/twython.git
cd twython
python setup.py install
```

## Documentation
Documentation is available at https://twython.readthedocs.io/en/latest/

## Starting Out
First, you'll want to head over to https://apps.twitter.com and register an application!

After you register, grab your applications `Consumer Key` and `Consumer Secret` from the application details tab.

The most common type of authentication is Twitter user authentication using OAuth 1. If you're a web app planning to have users sign up with their Twitter account and interact with their timelines, updating their status, and stuff like that this **is** the authentication for you!

First, you'll want to import Twython

```python
from twython import Twython
```

## Obtain Authorization URL
Now, you'll want to create a Twython instance with your `Consumer Key` and `Consumer Secret`:

- Only pass *callback_url* to *get_authentication_tokens* if your application is a Web Application
- Desktop and Mobile Applications **do not** require a callback_url

```python
APP_KEY = 'YOUR_APP_KEY'
APP_SECRET = 'YOUR_APP_SECRET'

twitter = Twython(APP_KEY, APP_SECRET)

auth = twitter.get_authentication_tokens(callback_url='http://mysite.com/callback')
```

From the `auth` variable, save the `oauth_token` and `oauth_token_secret` for later use (these are not the final auth tokens). In Django or other web frameworks, you might want to store it to a session variable

```python
OAUTH_TOKEN = auth['oauth_token']
OAUTH_TOKEN_SECRET = auth['oauth_token_secret']
```

Send the user to the authentication url, you can obtain it by accessing

```python
auth['auth_url']
```

## Handling the Callback
If your application is a Desktop or Mobile Application *oauth_verifier* will be the PIN code

After they authorize your application to access some of their account details, they'll be redirected to the callback url you specified in `get_authentication_tokens`.

You'll want to extract the `oauth_verifier` from the url.

Django example:

```python
oauth_verifier = request.GET['oauth_verifier']
```

Now that you have the `oauth_verifier` stored to a variable, you'll want to create a new instance of Twython and grab the final user tokens

```python
twitter = Twython(
    APP_KEY, APP_SECRET,
    OAUTH_TOKEN, OAUTH_TOKEN_SECRET
)

final_step = twitter.get_authorized_tokens(oauth_verifier)
```

Once you have the final user tokens, store them in a database for later use::

```python
    OAUTH_TOKEN = final_step['oauth_token']
    OAUTH_TOKEN_SECRET = final_step['oauth_token_secret']
```

For OAuth 2 (Application Only, read-only) authentication, see [our documentation](https://twython.readthedocs.io/en/latest/usage/starting_out.html#oauth-2-application-authentication).

## Dynamic Function Arguments
Keyword arguments to functions are mapped to the functions available for each endpoint in the Twitter API docs. Doing this allows us to be incredibly flexible in querying the Twitter API, so changes to the API aren't held up from you using them by this library.

Basic Usage
-----------

**Function definitions (i.e. get_home_timeline()) can be found by reading over twython/endpoints.py**

Create a Twython instance with your application keys and the users OAuth tokens

```python
from twython import Twython
twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
```

## Authenticated Users Home Timeline
```python
twitter.get_home_timeline()
```

## Updating Status
This method makes use of dynamic arguments, [read more about them](https://twython.readthedocs.io/en/latest/usage/starting_out.html#dynamic-function-arguments).

```python
twitter.update_status(status='See how easy using Twython is!')
```

## Advanced Usage
- [Advanced Twython Usage](https://twython.readthedocs.io/en/latest/usage/advanced_usage.html)
- [Streaming with Twython](https://twython.readthedocs.io/en/latest/usage/streaming_api.html)


## Questions, Comments, etc?
My hope is that Twython is so simple that you'd never *have* to ask any questions, but if you feel the need to contact me for this (or other) reasons, you can hit me up at ryan@venodesigns.net.

Or if I'm to busy to answer, feel free to ping mikeh@ydekproductions.com as well.

Follow us on Twitter:

- [@ryanmcgrath](https://twitter.com/ryanmcgrath)
- [@mikehelmick](https://twitter.com/mikehelmick)

## Want to help?
Twython is useful, but ultimately only as useful as the people using it (say that ten times fast!). If you'd like to help, write example code, contribute patches, document things on the wiki, tweet about it. Your help is always appreciated!
