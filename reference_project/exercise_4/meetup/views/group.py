from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from meetup.forms.group import GroupForm
from meetup.models import Group
from django.db.models import Count

tmpl = lambda *args: settings.CREATE_TEMPLATE_PATH('group', *args)


@login_required
def group_create(request):
    if request.method != "POST":
        form = GroupForm(request=request)
    else:
        form = GroupForm(request.POST, request=request)
        if form.is_valid():
            group = form.save(commit=False)
            group.creator = get_user_model().objects.get(pk=request.user.id)
            group.save()
            form.save_m2m()  # Required because of previous commit=False
            # Redirect to view the created group.
            return redirect('meetup:group_view', pk=group.pk)
        # Validation errors will automatically be propagated to the view.
    return render(request, tmpl('create.html'), {'form': form})


@login_required
def group_view(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.user not in group.members.all():
        msg = "You don't have permission to view this group."
        return HttpResponse(msg, mimetype='text/html')

    activities = (group.activities.annotate(num_votes=Count('votes'))
                                  .order_by('-num_votes'))
    # This will be horrendously horribly slow when there's any significant
    # amount of data. Oh well...
    for activity in activities:
        currentvote = activity.votes.filter(user__id=request.user.id)
        activity.current_vote = currentvote[0].vote if currentvote else None
        activity.up_votes = activity.votes.filter(vote=1).count()
        activity.down_votes = activity.votes.filter(vote=-1).count()
        activity.neutral_votes = activity.votes.filter(vote=0).count()

    return render(request, tmpl('view.html'), {'group': group,
                                               'activities': activities})


@login_required
def group_update(request, pk):
    group = get_object_or_404(Group, pk=pk)
    if request.user not in group.members.all():
        msg = "You don't have permission to edit this group."
        return HttpResponse(msg, mimetype='text/html')
    if request.method == 'POST':
        form = GroupForm(request.POST, request=request, instance=group)
        if form.is_valid():
            group = form.save()
            # Remove votes from users that are no longer in the group.
            for activity in group.activities.all():
                invalid_votes = activity.votes.exclude(
                    user__id__in=group.members.all())
                for invalid_vote in invalid_votes:
                    invalid_vote.delete()
            return redirect('meetup:group_view', pk=pk)
    else:
        form = GroupForm(instance=group, request=request)
    return render(request, tmpl('update.html'), {'form': form, 'group': group})
