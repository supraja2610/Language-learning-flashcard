from django.forms import ModelForm
from django.utils import timezone
from django.forms import widgets

from meetup.models import Activity
from meetup.mixins import SetErrorMixin


class ActivityForm(ModelForm, SetErrorMixin):
    class Meta:
        model = Activity
        fields = ['name', 'description', 'address', 'start_date', 'stop_date',
        'definite', 'image']
        widgets = {
            'description': widgets.Textarea,
            'start_date': widgets.DateTimeInput,
        }

    def clean(self):
        if (self.cleaned_data.get('stop_date', None) is None or
                self.cleaned_data.get('stop_date', None) is None):
            return self.cleaned_data
        # Make sure that start date is before stop date.
        if self.cleaned_data['stop_date'] < self.cleaned_data['start_date']:
            self.seterror('stop_date', "Your event can't stop before it starts.")

        # Make sure that the event takes place in the future.
        now = timezone.now()
        if self.cleaned_data['start_date'] < now:
            self.seterror('start_date', "Your event can't take place in the past!")
        if self.cleaned_data['stop_date'] < now:
            self.seterror('stop_date', "Your event can't take place in the past!")

        # Make sure that an event with the same name doesn't already exist.
        existing_activity = Activity.objects.filter(name=self.cleaned_data['name'],
                                                    start_date=self.cleaned_data['start_date'])
        if getattr(self.instance, 'pk', None):
            existing_activity = existing_activity.exclude(pk=self.instance.pk)
        if existing_activity:
            self.seterror('name', "You can't have two events by the same "
                                  "name that start at the same time.")
        return self.cleaned_data
