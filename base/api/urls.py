from django.urls import path,include
from django.conf import settings
from  . import views
from knox import views as knox_views 

urlpatterns = [
    (path('', views.allRoutes, name='api')),
    (path('groups/', views.allGroups, name='api-groups')),
    (path('friends/<str:friend_name>', views.GetPersonalMessage, name='api-personalmessages')),
    (path('groups/<str:group_id>', views.specificGroup, name='api-groupmessages')),
    (path('users/', views.allUsers, name='api-allusers')),
    (path('message/<str:username>', views.SendpersonalMessage, name='api-message-friend')),
    (path('message-group/<str:group_id>', views.SendGroupMessage, name='api-message-group')),
    (path('deletepersonalmessage/<str:message_id>', views.deletePersonalMessage, name='api-deletepersonalmessage')),
    (path('deletegroupmessage/<str:message_id>', views.deleteGroupMessage, name='api-deletegroupmessage')),
    (path('signin/' , views.signinUser, name='api-signin')),
    (path('signout/' , knox_views.LogoutAllView.as_view(), name='api-signout')),
    (path('personal-messages/<str:friend_name>' , views.GetPersonalMessage, name='api-personal-messages')),
]



