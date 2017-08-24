from django.forms import ModelForm, widgets
from meetup.models import UserProfile

class UserProfileUpdateForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['gender']