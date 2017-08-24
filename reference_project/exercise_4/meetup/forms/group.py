from meetup.models import Group
from meetup.mixins import SetErrorMixin
from meetup.custom_form import RequestModelForm
from django.forms.util import ErrorList
from django.forms import widgets

class GroupForm(RequestModelForm, SetErrorMixin):
    class Meta:
        model = Group
        fields = ['name', 'home', 'members', 'description']
        widgets = {
            'description': widgets.Textarea
        }

    def clean(self):
        if self.cleaned_data.get('name', None):
            # Make sure the creator doesn't already have a group with this name
            existing_groups = Group.objects.filter(creator__id=self.request.user.id,
                name=self.cleaned_data['name'])

            if getattr(self.instance, 'pk', None):
                existing_groups = existing_groups.exclude(pk=self.instance.pk)


        # Make sure that the creator is himself a member of the group.
        if self.cleaned_data.get('members', None):
            if self.request.user not in self.cleaned_data['members']:
                errors = self._errors.setdefault("members", ErrorList())
                errors.append(u'You have to add yourself as a member of the group')

        return self.cleaned_data
