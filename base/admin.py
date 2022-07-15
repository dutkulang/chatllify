from django.contrib import admin
from .models import Profiles, friends, groupstable, groupmessages, personalmessages

admin.site.register(Profiles)
admin.site.register(friends)
admin.site.register(groupstable)
admin.site.register(groupmessages)
admin.site.register(personalmessages)
