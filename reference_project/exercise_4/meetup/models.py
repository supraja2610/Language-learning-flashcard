from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

MAX_NAME_LENGTH = 75
MAX_ADDRESS_LENGTH = 200
MAX_URL_LENGTH = 200
MAX_DESCRIPTION_LENGTH = 1000

GENDER_CHOICES = (
    ('m', 'Male'),
    ('f', 'Female')
);

class UserProfile(models.Model):
    # An id field is added automatically by Django

    """ `User` of the application
    """
    user = models.OneToOneField(User, null=False, on_delete=models.CASCADE,
        related_name='user')


    """ Gender of the `User`
    """
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)


    """ Avatar of the `User`
    """
    avatar = models.URLField(max_length=MAX_URL_LENGTH)


    """ Twitter access token of the `User`
    """
    twitter_token = models.CharField(max_length=MAX_URL_LENGTH, blank=True)

    def __unicode__(self):
        return '%s' % (self.user)

    def create_user_profile(sender, instance, created, raw, using, update_fields, **kwargs):
        if created:
            profile = UserProfile()
            profile.user = instance
            profile.save()

    post_save.connect(create_user_profile, sender=User)


class Group(models.Model):
    # An id field is added automatically by Django.


    """ Name of the group.
    This field is also referred to as 'topic' in the exercise description.

    """
    name = models.CharField(max_length=MAX_NAME_LENGTH, blank=False, unique=True)


    """ `User` who created the group.

    """
    creator = models.ForeignKey(User, null=False,
        on_delete=models.CASCADE, related_name='creator')


    """ Home address of the group.
    This is most likely in the area where the creator lives.

    """
    home = models.CharField(max_length=MAX_ADDRESS_LENGTH, blank=False)


    """ Date at which the group was created.
    This field is set automatically, and should not be editable by users.

    """
    created = models.DateTimeField(auto_now_add=True)


    """ Description of the group.
    """
    description = models.CharField(max_length=MAX_DESCRIPTION_LENGTH, blank=False)


    """ Indicating the maximum number of votes each member can vote
    The default value 0 means that there is not limitation
    """
    vote_limit = models.SmallIntegerField(blank=False, default=0)


    """ The members of the group.
    These are added by the `creator`.

    """
    members = models.ManyToManyField(User, null=False, related_name='members')

    def __unicode__(self):
        return self.name


class Activity(models.Model):
    # An id field is added automatically by Djaongo.


    """ Name of the activity.

    """
    name = models.CharField(max_length=MAX_NAME_LENGTH, blank=False)


    """ A description of the `Activity`.
    This is where a user would explain to other users further details on
    what exactly is going to happen in the event.

    """
    description = models.CharField(max_length=MAX_DESCRIPTION_LENGTH, blank=False)


    """ The `Group` to which the activity belongs.

    """
    group = models.ForeignKey(Group, null=False, on_delete=models.CASCADE,
        related_name='activities')


    """ The address at which the activity takes place.
    This field shall contain an address which can be looked up on google maps,
    to which there will automatically be generated a link.

    """
    address = models.CharField(max_length=MAX_ADDRESS_LENGTH, blank=False)


    """ The point in time in which the `Activity` starts.

    """
    start_date = models.DateTimeField(blank=False)


    """ The point in time in which the `Activity` is planned to stop.
    This is given as a date, and will be used to calculate a duration.

    """
    stop_date = models.DateTimeField(blank=False)


    """ The image of the `Activity`
    """
    image = models.URLField(max_length=MAX_URL_LENGTH, blank=False)


    """ Indicating whether the `Activity` is definite or not.
    A definite event is one that _has been decided_ to take place by
    the creator.

    """
    definite = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name


class Vote(models.Model):

    """ Vote model used to support voting functionality in the `Activity` model.
    This model represents votes in a "reddit-fashion", allowing users to cast
    one up- or downvote.

    """

    # An id field is added automatically by Djaongo.


    """ The `User` that cast the vote.

    """
    user = models.ForeignKey(User, null=False,
        on_delete=models.CASCADE, related_name='voter')


    """ Indicating whether the vote was up (1), down (-1) or neutral (0).

    """
    vote = models.SmallIntegerField()


    """ The activity on which the vote was cast.

    """
    activity = models.ForeignKey(Activity, null=False, on_delete=models.CASCADE,
        related_name='votes')
