from django.urls import path,include
from django.conf import settings
from  . import views

urlpatterns = [
    (path('', views.allRoutes, name='api')),
    (path('my_groups/', views.allRoutes, name='my-groups')),
    (path('groups/', views.allGroups, name='groups')),
    (path('friends/', views.allRoutes, name='my-friends')),
    (path('friends/<str:friend_name>', views.GetPersonalMessage, name='personalmessages')),
    (path('groups/<str:group_id>', views.specificGroup, name='groupmessages')),
    (path('users/', views.allUsers, name='allusers')),
    (path('message/<str:username>', views.SendpersonalMessage, name='message-friend')),
    (path('message-group/<str:group_id>', views.SendGroupMessage, name='message-group')),
    (path('deletepersonalmessage/<str:message_id>', views.deletePersonalMessage, name='deletepersonalmessage')),
    (path('deletegroupmessage/<str:message_id>', views.deleteGroupMessage, name='deletegroupmessage')),
]



