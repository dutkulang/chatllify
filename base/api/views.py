#from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import GroupMessagesSerialiazer, ProfilesSerializer, PersonalMessagesSerializer, SendPersonalMessagesSerializer
from base.models import groupmessages, Profiles, personalmessages
from django.db.models import Q
from knox.auth import AuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
def allRoutes(request):
    routes = {
        'route - api':'/api',
        'route - authenticate':'/api/signin',
        'route - all groups': '/api/groups',
        'route - all users': '/api/users',
        'route - query specific users': '/api/users/::query',
        'route - query specific groups': '/api/groups/::query',
        'route - specific group messages': '/api/groups/::group_id',
        'route - specific personal messages': '/api/friends/::friend_name',
        'route - delete personal message': '/api/deletepersonalmessage/::message_id',
        'route - delete group message': '/api/deletegroupmessage/::message_id',
        'route - logout':'api/signout'
    }
    return Response(routes)

@api_view(['POST'])
def signinUser(request):
    serializer = AuthTokenSerializer(data=request.POST)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    created ,token = AuthToken.objects.create(user)
    return Response({'user info':{'user_id': user.id , 'email': user.email}, 'token': token})

@api_view(['GET'])
def allGroups(request):
    if request.user.is_authenticated:
        groups = groupmessages.objects.all()
        serializer = GroupMessagesSerialiazer(groups,many=True)
        return Response(serializer.data)
    return Response('User needs to be authenticated to access this information')

@api_view(['GET'])
def specificGroup(request,group_id):
    if request.user.is_authenticated:
        groups = groupmessages.objects.get(id=group_id)
        serializer = GroupMessagesSerialiazer(groups, many=False)
        return Response(serializer.data)
    return Response('User needs to be authenticated to access this information')

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
def allUsers(request):
    users = Profiles.objects.all()
    serializer =  ProfilesSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def SendpersonalMessage(request,username):
    if request.user.is_authenticated:
        user = Profiles.objects.get(id=request.user.id)
        try:
            friend = Profiles.objects.get(name=username)
        except:
            return Response('Recipient user does not exist!')
        check_friend =  True if friend.name in [x.profile.name for x in user.user_friends.all()] else False
        if check_friend:
            serializer = PersonalMessagesSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        return Response('you have to be friends with this user to send messages!')
    return Response('User needs to be authenticated to access this information')

@api_view(['POST'])
def SendGroupMessage(request,group_id):
    if request.user.is_authenticated:
        user = Profiles.objects.get(id=request.user.id)
        try:
            group = groupmessages.objects.get(id=group_id)
        except:
            return Response('group does not exist!')
        if user in group.participants.all():
            serializer = GroupMessagesSerialiazer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors)
        return Response('you need to be a member of the group first inorder to send messages!')
    return Response('User needs to be authenticated to access this information')

@api_view(['GET'])
def GetPersonalMessage(request,friend_name):
    if request.user.is_authenticated:
        messages = personalmessages.objects.filter(
        (Q(sender__name = request.user.username) & Q(reciever__name = friend_name)) |
        (Q(sender__name = friend_name) & Q(reciever__name = request.user.username))).order_by('time')
        serializer = PersonalMessagesSerializer(messages, many=True)
        return Response(serializer.data)
    return Response('User needs to be authenticated to access this information')

@api_view(['DELETE'])
def deletePersonalMessage(request,message_id):
    if request.user.is_authenticated:
        message = personalmessages.objects.get(id=message_id)
        message.delete()
        return Response('Messsage deleted successfully')
    return Response('User needs to be authenticated to access this information')

@api_view(['DELETE'])
def deleteGroupMessage(request,message_id):
    if request.user.is_authenticated:
        message = groupmessages.objects.get(id=message_id)
        message.delete()
        return Response('Messsage deleted successfully')
    return Response('User needs to be authenticated to access this information')



