from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index' ),
    path('home/',views.home, name='home' ),

    path('messages/<str:friend_username>',views.personal_messages, name='messages' ),
    path('groups/<str:group_id>',views.group_and_messages, name='groups' ),
    path('friends/', views.all_friends, name='all_friends' ),
    path('groups/', views.all_groups, name='all_groups' ),

    path('store_group_message', views.store_group_message, name='store_group_message' ),
    path('return_group_messages/<str:group_id>', views.return_group_messages , name='return_group_messages'),
    path('delete_group/<str:group_id>',views.delete_group, name='delete_group' ),
    path('delete_group_message/<str:message_id>',views.delete_group_message, name='delete_group_message' ),
    path('join_group/<str:group_id>',views.join_group, name='join_group'),

    path('store_personal_messages', views.store_personal_messages , name='store_personal_messages'),
    path('retrieve_personal_messages/<str:friend_username>', views.retrieve_personal_messages , name='retrieve_personal_messages'),

    path('update_profile', views.update_profile , name='update_profile'),

    path('signup/',views.SignUp, name='signup' ),
    path('signin/',views.SignIn, name='signin' ),
    path('settings/',views.settings, name='settings' ),
    path('logout/',views.signout, name='signout' ),
    path('delete_account/',views.delete_account, name='delete_account' )
]




