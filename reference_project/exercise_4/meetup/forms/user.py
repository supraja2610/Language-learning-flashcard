from django.forms import ModelForm, widgets
from django.contrib.auth import get_user_model

class UserCreateForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'password', 'first_name', 'last_name', 'email']
        widgets = {
            'password': widgets.PasswordInput
        }

class UserUpdateForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']