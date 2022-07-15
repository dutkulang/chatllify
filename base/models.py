from django.db import models
from django.contrib.auth.models import User

class Profiles(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    name = models.CharField(max_length=50,default='None')
    password = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    profile_pics = models.CharField(max_length=200,default='image.jpg')
    date_joined = models.DateTimeField(auto_now_add=True)
    about = models.CharField(max_length=50, default='Hi')
    user_friends = models.ManyToManyField('friends',related_name='my_friends', blank=True)

class friends(models.Model):
    profile = models.ForeignKey(Profiles,on_delete=models.CASCADE,related_name='users')

class groupstable(models.Model):
    owner = models.ForeignKey(Profiles,on_delete=models.CASCADE)
    title = models.CharField(max_length=200,default='JUST CREATED!')
    participants = models.ManyToManyField(Profiles,related_name='group_participants',blank=True)

class groupmessages(models.Model):
    owned_group = models.ForeignKey(groupstable,on_delete=models.CASCADE)
    message_sender = models.ForeignKey(Profiles,on_delete=models.CASCADE)
    message_body = models.CharField(max_length=2000)
    time_sent = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-time_sent']

class personalmessages(models.Model):
    sender = models.ForeignKey(Profiles,on_delete=models.CASCADE)
    reciever = models.ForeignKey(Profiles,on_delete=models.CASCADE,related_name='reciever_id')
    message_body = models.CharField(max_length=2000)
    time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['time']

