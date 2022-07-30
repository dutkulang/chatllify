from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import ProfileForm, PersonalMessageForm, AccountSettingsForm
from .models import Profiles, friends, groupstable, groupmessages, personalmessages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import os
import numpy as np
import cv2 as cv
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent


def index(request):

    return render(request,'index.html')

@login_required(login_url='/signin')
def home(request):
    user = Profiles.objects.get(name=request.user.username)
    groups = groupstable.objects.filter(participants=user)
    messages = personalmessages.objects.filter(Q(sender=user)|
                                               Q(reciever=user))
    context = {'user':user,'messages':messages[:12],'groups':groups[:4]}

    return render(request,'home.html',context=context)

def SignUp(request):
    form = ProfileForm()
    context = {'form':form}
    if request.method=='POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(email=email):
            print('email exists already')
        else:
            if User.objects.filter(username=name):
                print('username exists already')
            else:
                if password == confirm_password:
                    new_user = User.objects.create_user(username=name,email=email,password=password)
                    new_user.save()

                    # create profile instance
                    user = User.objects.get(email=email)
                    new_profile = Profiles(user=user,name=name)
                    new_profile.save()
                    
                    # create a friends instance 
                    profile = Profiles.objects.get(name=name)
                    friends.objects.create(profile=profile)

                    # create default profile image
                    profile_image_generator(profile.id)

                    print('all actions successful....')
                    login(request, user)
                    return redirect('/home')
                else:
                    print('password must match')

    return render(request,'signup.html',context=context)

def profile_image_generator(user_id,profile_images_path=os.path.join(BASE_DIR,'media/profile_images')):
    os.chdir(profile_images_path)
    blank_img = np.zeros((150, 150, 3), dtype='uint8')
    try:
        cv.imwrite(f'{user_id}.jpg', blank_img)
    except:
        pass

def SignIn(request):

    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user_authentication = authenticate(request,username=username, password=password)
        if user_authentication:
            login(request, user_authentication)
            return redirect('/home')
        else:
            print('Invalid username or password')

    return render(request,'signin.html')

def signout(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/signin')
def personal_messages(request,friend_username):

    friend = Profiles.objects.get(name=friend_username)
    user = Profiles.objects.get(name=request.user.username)
    friend_profile = friends.objects.get(profile__name=friend_username)
    
    context = {'friend':friend,'user':user,'user':user,'friend_profile':friend_profile}
    return render(request,'messages.html',context=context)


def store_personal_messages(request):
    friend_username = request.POST['friend_username']
    message_body = request.POST['message_body']

    friend = Profiles.objects.get(name=friend_username)
    user = Profiles.objects.get(name=request.user.username)

    # checks if friend in the users friends through username .... usernames should be unique
    friend_check = True if friend.name in [x.profile.name for x in user.user_friends.all()] else False
    if friend_check:
        new_message = personalmessages(sender=user,reciever=friend,message_body=message_body)
        new_message.save()

    return HttpResponse('successful')

def delete_personal_message(request,message_id):
    message = personalmessages.objects.get(id=message_id)
    message.delete()
    return redirect(f'/messages/{message.reciever.name}')

def add_friend(request,friend_username):
    user = Profiles.objects.get(name=request.user.username)
    attempted_friend = friends.objects.get(profile__name=friend_username)
    user.user_friends.add(attempted_friend)
    return redirect(f'/messages/{friend_username}')

def delete_friend(request,friend_username):
    user = Profiles.objects.get(name=request.user.username)
    deleted_friend = friends.objects.get(profile__name=friend_username)
    # print(deleted_friend in user.user_friends.all())
    user.user_friends.remove(deleted_friend)
    return redirect('/home')

def retrieve_personal_messages(request,friend_username):

    friend = Profiles.objects.get(name=friend_username)
    user = Profiles.objects.get(name=request.user.username)

    messages = personalmessages.objects.filter(
        (Q(sender = user) & Q(reciever = friend)) |
        (Q(sender = friend) & Q(reciever = user))
    ).order_by('time')
    
    return JsonResponse({"messages":list(messages.values())})

@login_required(login_url='/signin')
def CreateGroups(request):
    user = Profiles.objects.get(name=request.user.username)
    title = request.POST.get('title')
    new_group = groupstable(owner=user,title=title)
    new_group.save()
    new_group.participants.add(user)

    # flash group created successfully
    # redirect back to within the group
    return HttpResponse('heres my groups')


@login_required(login_url='/signin')
def group_and_messages(request,group_id):
    user = Profiles.objects.get(name = request.user.username)
    group = groupstable.objects.get(id=group_id)
    
    context = {'user':user,'group':group,'group_id':group_id}
    return render(request,'groupmessages.html',context=context)


def store_group_message(request):
    user = Profiles.objects.get(name=request.user.username)
    message_body = request.POST['message_body']
    owned_group = request.POST['group_id']

    group = groupstable.objects.get(id=owned_group)
    if user in group.participants.all():
        new_message = groupmessages(owned_group=group,message_sender=user,message_body=message_body)
        new_message.save()

        print('successful')
    return HttpResponse('successful')


def return_group_messages(request,group_id):
    group = groupstable.objects.get(id=group_id)

    group_messages = groupmessages.objects.filter(owned_group=group)

    return JsonResponse({"group_messages":list(group_messages.values())})

def delete_group_message(request,message_id):
    message = groupmessages.objects.get(id=message_id)
    group_id = message.owned_group.id
    message.delete()
    return redirect(f'/groups/{group_id}')

def delete_group(request,group_id):
    user = Profiles.objects.get(id=request.user.id)
    group = groupstable.objects.get(id=group_id)
    if user == group.owner:
        group.delete()
        return redirect('/groups')
    return redirect('/groups')

def join_group(request,group_id):
    user = Profiles.objects.get(name=request.user.username)
    group = groupstable.objects.get(id=group_id)
    group.participants.add(user)
    return redirect(f'/groups/{group_id}')

def leave_group(request,group_id):
    user = Profiles.objects.get(name=request.user.username)
    group = groupstable.objects.get(id=group_id)
    group.participants.remove(user)
    return redirect('/groups')

@login_required(login_url='/signin')
def all_groups(request):
    user = Profiles.objects.get(name=request.user.username)
    groups_data = groupstable.objects.filter(participants=user)
    query_track = False
    
    query = request.GET.get('q')
    q = query if query else ''
    if query:
        groups_data = groupstable.objects.filter(Q(title__icontains=q)) #| Q(groupmessages__message_body__icontains=q))
        query_track = True

    context = {'groups_data':groups_data,'query_track':query_track,'user':user}
    
    return render(request,'groupsquerypage.html',context=context)


@login_required(login_url='/signin')
def all_friends(request):
    user = Profiles.objects.get(name=request.user.username)
    all_profiles = Profiles.objects.all()
    current_user_friends = [ users.profile for users in user.user_friends.all() ]
    all_users = user.user_friends.all()
    query_track = False

    query = request.GET.get('q')
    q = query if query else ''
    if query:
        all_users = Profiles.objects.filter(name__icontains=q)  # all users display done
        query_track = True
    
    context = {'all_users':all_users,'query_track':query_track,'current_user_friends':current_user_friends,'all_profiles':all_profiles}
    return render(request,'usersquerypage.html',context=context)


# @login_required(login_url='/signin')
# def addfriend(request,friend_id):
#     user = Profiles.objects.get(id=request.user.id)
#     friend = Profiles.objects.get(id=friend_id)
#     user.friends.add(friend)

@login_required(login_url='/signin')
def settings(request):
    
    user = Profiles.objects.get(name=request.user.username)
    groups = groupstable.objects.filter(participants=user).count()
    form = AccountSettingsForm()
    updatable = False
    if request.method == 'POST' and updatable == False:
        updatable = True

    context = {'user':user,'groups':groups,'updatable':updatable,'form':form}

    return render(request,'settings.html',context=context)

def profile_image_handler(user_id,uploaded_file_name,profile_images_path=os.path.join(BASE_DIR,'media/profile_images')):
    os.chdir(profile_images_path)
    try:
        os.remove(f'{user_id}.jpg')
    except:
        pass
    os.rename(f'{uploaded_file_name}',f'{user_id}.jpg')

def update_profile(request):
    user = User.objects.get(username=request.user.username)
    profile = Profiles.objects.get(name=request.user.username)

    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    about = request.POST['about']
    profile_img = request.FILES.get('profile_picture')

    new_username = username #if username else user.username
    if new_username:
        if new_username in [profile.name for profile in Profiles.objects.all()] and new_username != request.user.username:
            return HttpResponse('Username taken !')
            
    new_username = username if username else user.username
    new_email = email if email else user.email
    new_about = about if about else profile.about
    new_profile_img = profile_img if profile_img else profile.profile_pics

    if password:
        user.set_password(password)
    user.username = new_username
    user.email = new_email
    
    user.save()

    profile.name = new_username 
    profile.about = new_about
    profile.profile_pics = new_profile_img
    profile.save()

    if profile_img:
        print(profile_image_handler( profile.id, new_profile_img.name))

    return redirect('/settings')

def delete_account(request):
    user = User.objects.get(id=request.user.id)
    user.delete()
    return redirect('/')





