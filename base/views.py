from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .forms import ProfileForm, PersonalMessageForm
from .models import Profiles, friends, groupstable, groupmessages, personalmessages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib.auth.decorators import login_required


def index(request):

    return render(request,'index.html')

@login_required(login_url='/signin')
def home(request):
    user = Profiles.objects.get(id=request.user.id)
    groups = groupstable.objects.filter(participants=user)
    messages = personalmessages.objects.filter(Q(sender=user)|
                                               Q(reciever=user))
    context = {'user':user,'messages':messages,'groups':groups}

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
                    new_user = User.objects.create(username=name,email=email,password=password)

                    user = User.objects.get(email=email)
                    new_profile = Profiles(user=user,name=name,email=email,password=password)
                    new_profile.save()

                    profile = Profiles.objects.get(email=email)
                    friends.objects.create(profile=profile)

                    print('all actions successful....')
                else:
                    print('password must match')

    # user = Profiles.objects.get(id=request.user.id)
    # print(groupstable.objects.filter(participants=user))  ### my groups

    return render(request,'signup.html',context=context)

def SignIn(request):

    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        print(username,password)
        usilo = User.objects.get(username=username)
        print(usilo.username,usilo.password)

        user_authentication = authenticate(request,username=username, password=password)
        if user_authentication:
            login(request, user_authentication)
            print('login successful')
        else:
            print('Invalid username or password')

    return render(request,'signin.html')

def signout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='/signin')
def personal_messages(request,friend_username):

    friend = Profiles.objects.get(name=friend_username)
    user = Profiles.objects.get(id=request.user.id)

    context = {'friend':friend,'user':user,'Check':Check,'user':user}
    return render(request,'messages.html',context=context)


def store_personal_messages(request):
    friend_username = request.POST['friend_username']
    message_body = request.POST['message_body']

    friend = Profiles.objects.get(name=friend_username)
    user = Profiles.objects.get(id=request.user.id)

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
    user = Profiles.objects.get(id=request.user.id)
    attempted_friend = Profiles.objects.get(name=friend_username)
    user.user_friends.add(attempted_friend)
    return redirect('messages/friend_username')

def delete_friend(request,friend_username):
    user = Profiles.objects.get(id=request.user.id)
    deleted_friend = Profiles.objects.get(name=friend_username)
    user.user_friends.delete(deleted_friend)
    return redirect('/home')

def retrieve_personal_messages(request,friend_username):

    friend = Profiles.objects.get(name=friend_username)
    user = Profiles.objects.get(id=request.user.id)

    messages = personalmessages.objects.filter(
        (Q(sender = user) & Q(reciever = friend)) |
        (Q(sender = friend) & Q(reciever = user))
    )
    
    return JsonResponse({"messages":list(messages.values())})

@login_required(login_url='/signin')
def CreateGroups(request):
    user = Profiles.objects.get(id=request.user.id)
    title = request.POST.get('title')
    new_group = groupstable(owner=user,title=title)
    new_group.save()
    new_group.participants.add(user)

    # flash group created successfully
    # redirect back to within the group
    return HttpResponse('heres my groups')


@login_required(login_url='/signin')
def group_and_messages(request,group_id):
    user = Profiles.objects.get(id = request.user.id)
    group = groupstable.objects.get(id=group_id)
    
    context = {'user':user,'group':group,'group_id':group_id}
    return render(request,'groupmessages.html',context=context)


def store_group_message(request):
    user = Profiles.objects.get(id=request.user.id)
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
    message.delete()

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

@login_required(login_url='/signin')
def all_groups(request):
    user = Profiles.objects.get(id=request.user.id)
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
    user = Profiles.objects.get(id=request.user.id)
    current_user_friends = [ users.profile for users in user.user_friends.all() ]
    all_users = user.user_friends.all()
    query_track = False

    query = request.GET.get('q')
    q = query if query else ''
    if query:
        all_users = Profiles.objects.filter(name__icontains=q)  # all users display done
        query_track = True
    
    context = {'all_users':all_users,'query_track':query_track,'current_user_friends':current_user_friends}
    return render(request,'usersquerypage.html',context=context)


# @login_required(login_url='/signin')
# def addfriend(request,friend_id):
#     user = Profiles.objects.get(id=request.user.id)
#     friend = Profiles.objects.get(id=friend_id)
#     user.friends.add(friend)


@login_required(login_url='/signin')
def settings(request):
    
    user = Profiles.objects.get(id=request.user.id)
    groups = groupstable.objects.filter(participants=user).count()
    updatable = False
    if request.method == 'POST' and updatable == False:
        updatable = True

    context = {'user':user,'groups':groups,'updatable':updatable}

    return render(request,'settings.html',context=context)

def update_profile(request):
    user = User.objects.get(username=request.user.username)
    profile = Profiles.objects.get(name=request.user.username)

    username = request.POST['username']
    email = request.POST['email']
    password = request.POST['password']
    about = request.POST['about']


    new_username = username if username else user.username
    new_email = email if email else profile.email
    new_password = password if password else user.password
    new_about = about if about else profile.about

    profile.name = new_username 
    profile.email = new_email
    profile.password = new_password
    profile.about = new_about

    profile.save()

    return redirect('/settings')

def delete_account(request):
    user = User.objects.get(id=request.user.id)
    user.delete()
    return redirect('/')





