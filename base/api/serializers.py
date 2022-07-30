from base.models import groupmessages, Profiles, personalmessages
from rest_framework.serializers import ModelSerializer

class GroupMessagesSerialiazer(ModelSerializer):
    class Meta:
        model = groupmessages
        fields = "__all__"

class ProfilesSerializer(ModelSerializer):
    class Meta:
        model = Profiles
        fields = ['name','profile_pics','date_joined','about','date_joined']

class PersonalMessagesSerializer(ModelSerializer):
    class Meta:
        model = personalmessages
        fields = "__all__"

class SendPersonalMessagesSerializer(ModelSerializer):
    class Meta:
        model = personalmessages
        fields = ['sender','reciever','message_body']


