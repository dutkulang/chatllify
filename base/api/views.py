#from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import GroupMessagesSerialiazer, ProfilesSerializer, PersonalMessagesSerializer, SendPersonalMessagesSerializer
from base.models import groupmessages, Profiles, personalmessages
from django.db.models import Q

@api_view(['GET'])
def allRoutes(request):
    routes = {
        'route - api':'/api',
        'route - authenticate [sign-in]':'/api/signin',
        'route - friends': '/api/friends',
        'route - my groups': '/api/groups',
        'route - query users': '/api/users/::query',
        'route - query groups': '/api/groups/::query',
        'route - specific group messages': '/api/groups/::group_id',
        'route - specific personal messages': '/api/friends/::friend_name',
        'route - delete personal message': '/api/deletepersonalmessage/::message_id',
        'route - delete group message': '/api/deletegroupmessage/::message_id'

    }
    return Response(routes)

@api_view(['GET'])
def allGroups(request):
    groups = groupmessages.objects.all()
    serializer = GroupMessagesSerialiazer(groups,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def specificGroup(request,group_id):
    groups = groupmessages.objects.get(id=group_id)
    serializer = GroupMessagesSerialiazer(groups, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def allUsers(request):
    users = Profiles.objects.all()
    serializer =  ProfilesSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def SendpersonalMessage(request,username):
    serializer = PersonalMessagesSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['POST'])
def SendGroupMessage(request,group_id):
    serializer = GroupMessagesSerialiazer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)

@api_view(['GET'])
def GetPersonalMessage(request,friend_name):
    messages = personalmessages.objects.filter(Q(reciever__name=friend_name)|
                                               Q(sender__name=friend_name))
    serializer = PersonalMessagesSerializer(messages, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def deletePersonalMessage(request,message_id):
    message = personalmessages.objects.get(id=message_id)
    message.delete()
    return Response('Messsage deleted successfully')

@api_view(['DELETE'])
def deleteGroupMessage(request,message_id):
    message = groupmessages.objects.get(id=message_id)
    message.delete()
    return Response('Messsage deleted successfully')



