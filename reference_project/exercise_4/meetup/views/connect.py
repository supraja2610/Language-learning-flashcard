from django.conf import settings
from django.http import *
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from meetup.models import UserProfile

import tweepy

tmpl = lambda *args: settings.CREATE_TEMPLATE_PATH('connect', *args)

TWITTER_API_KEY = '96IQD6ArC3YbmyaVMuXAI9e5l'
TWITTER_API_SECRET = 'WILrG8D2CdZ5LG3fDfE38bY7uv4BJOkQy4YUeTZDr5w0zr9Edu'

@login_required
def twitter_request(request):
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    try:
        url = auth.get_authorization_url()
        request.session['twitterToken'] = (auth.request_token.key, auth.request_token.secret)
        return redirect(url)
    except tweepy.TweepError:
        pass
    else:
        pass
    finally:
        pass

    return render(request, tmpl('twitter.html'), {})

@login_required
def twitter_access(request):
    oauthToken = request.GET['oauth_token']
    oauthVerifier = request.GET['oauth_verifier']
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    token = request.session['twitterToken']
    del request.session['twitterToken']
    auth.set_request_token(token[0], token[1])

    try:
        accessToken = auth.get_access_token(oauthVerifier)
        profileSet = UserProfile.objects.filter(user__id=request.user.id)
        if profileSet:
            profile = profileSet[0]
            profile.twitter_token = accessToken
            profile.save()

        return render(request, tmpl('twitter.html'), {'connected': True})
    except tweepy.TweepError:
        pass
    else:
        pass
    finally:
        pass

    return render(request, tmpl('twitter.html'), {})

@login_required
def twitter_disconnect(request):

    profileSet = UserProfile.objects.filter(user__id=request.user.id)
    if profileSet:
        profile = profileSet[0]
        profile.twitter_token = ""
        profile.save()

    return render(request, tmpl('twitter.html'), {'disconnected': True})