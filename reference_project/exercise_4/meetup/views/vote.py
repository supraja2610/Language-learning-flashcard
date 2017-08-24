from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404

from meetup.models import Vote, Activity


@login_required
def vote(request, group_pk, activity_pk, value):
    """ Vote on an activity.
    `value` indicates which vote is being cast; 1 is positive, -1 is negative,
    and 0 is neutral.
    """
    voteset = Vote.objects.filter(user__id=request.user.id,
                                  activity__pk=activity_pk)
    if voteset:
        vote = voteset[0]
    else:
        # User has not voted yet.
        activity = get_object_or_404(Activity, pk=activity_pk)
        vote = Vote(user=request.user, activity=activity, vote=value)
    vote.vote = value
    vote.save()
    return redirect('meetup:group_view', pk=group_pk)
