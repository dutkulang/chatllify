from django.forms import ModelForm
from .models import Profiles, groupstable, groupmessages, personalmessages

class ProfileForm(ModelForm):
    class Meta:
        model = Profiles
        fields = ['name','email','password']

class PersonalMessageForm(ModelForm):
    class Meta:
        model = personalmessages
        fields = ['message_body']

