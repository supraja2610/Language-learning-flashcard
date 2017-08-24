from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from meetup.forms.activity import ActivityForm
from meetup.models import Group, Activity
from meetup.models import UserProfile

import logging
import tweepy
import re

tmpl = lambda *args: settings.CREATE_TEMPLATE_PATH('activity', *args)

TWITTER_API_KEY = '96IQD6ArC3YbmyaVMuXAI9e5l'
TWITTER_API_SECRET = 'WILrG8D2CdZ5LG3fDfE38bY7uv4BJOkQy4YUeTZDr5w0zr9Edu'


def twitter_key_parse(token):
    key = ''
    m = re.match(r'oauth_token_secret=(.*?)&', token, re.M | re.I)
    if m:
        key = m.group(1)
    return key


def twitter_token_parse(token):
    start_index = token.rfind('=')
    auth_token = token[start_index + 1:]
    return auth_token


def tweet(request, group, activity):
    profile = request.user.get_profile()
    if not request.user.get_profile().twitter_token:
        return
    twitter_token = profile.twitter_token
    twitter_key = twitter_key_parse(twitter_token)
    twitter_token = twitter_token_parse(twitter_token)
    auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
    auth.set_access_token(twitter_token, twitter_key)
    api = tweepy.API(auth)
    api.update_status("{group}'s activity {activity} has become DEFINITE!"
                      "".format(group=group.name, activity=activity.name))


@login_required
def activity_create(request, group_pk):
    group = get_object_or_404(Group, pk=group_pk)
    if request.user  == group.creator.id:
        msg = "You don't have permission to create an activity in this group."
        return HttpResponse(msg, mimetype='text/html')
    if request.method != "POST":
        form = ActivityForm()
    else:
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.group = group
            activity.save()
            form.save_m2m()  # Required because of previous commit=False.

            if activity.definite:
                    tweet(request, group, activity)

            return redirect('meetup:group_view', pk=group_pk)
        # Validation errors will automatically be propagated to the view.
    return render(request, tmpl('create.html'), {'form': form, 'group': group})


@login_required
def activity_view(request, pk, group_pk):
    group = get_object_or_404(Group, pk=group_pk)
    if request.user not in group.members.all():
        msg = "You don't have permission to view this activity."
        return HttpResponse(msg, mimetype='text/html')
    activity = get_object_or_404(Activity, pk=pk)
    return render(request, tmpl('view.html'),
                  {'activity': activity, 'group': group,
                   'duration': activity.stop_date - activity.start_date})


@login_required
def activity_update(request, pk, group_pk):
    activity = get_object_or_404(Activity, pk=pk)
    previous_status = activity.definite
    group = get_object_or_404(Group, pk=group_pk)
    if not request.user.id == group.creator.id:
        msg = "You don't have permission to edit this activity."
        return HttpResponse(msg, mimetype='text/html')
    if request.method != "POST":
        form = ActivityForm(instance=activity)
    else:
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            if not previous_status and activity.definite:
                tweet(request, group, activity)
            return redirect('meetup:activity_view', pk=pk, group_pk=group_pk)
    return render(request, tmpl('update.html'),
                  {'form': form, 'group': group, 'activity': activity})
