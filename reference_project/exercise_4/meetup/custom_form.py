from django.forms import ModelForm

class RequestModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(RequestModelForm, self).__init__(*args, **kwargs)
