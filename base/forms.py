from django.forms import ModelForm, Form
from django import forms
from .models import Profiles, groupstable, groupmessages, personalmessages

class ProfileForm(Form):
    # class Meta:
    #     model = Profiles
    #     fields = ['name','email','password']
    name = forms.CharField(min_length=3, max_length=20)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

class PersonalMessageForm(ModelForm):
    class Meta:
        model = personalmessages
        fields = ['message_body']

class AccountSettingsForm(Form):
    username = forms.CharField(min_length=3,max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())
    profile_picture = forms.ImageField()
    about = forms.CharField(max_length=50)
    email = forms.EmailField()
    

