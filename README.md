# chatllify
An async chat application in django

A real time chat application using the Django framework and AJAX

Rest API *[https://chatllify.herokuapp.com/api/]* - Auth (django-knox) , API (django-rest-framework) 

*Routes : {
    "route - api": "/api",
    "route - authenticate": "/api/signin/",
    "route - all groups": "/api/groups/",
    "route - my-groups": "/api/my-groups/",
    "route - all users": "/api/users/",
    "route - query specific users": "/api/users/::query/",
    "route - query specific groups": "/api/groups/::query/",
    "route - specific group messages": "/api/groups/::group_id/",
    "route - specific personal messages": "/api/friends/::friend_name/",
    "route - delete personal message": "/api/deletepersonalmessage/::message_id/",
    "route - delete group message": "/api/deletegroupmessage/::message_id/",
    "route - logout": "api/signout"
}*

postman :

1. authenticate https://chatllify.herokuapp.com/api/signin/

{'token': 'your secret generated token'}

app :

git clone repo--

pip install -r requirements.txt

#### ![Screenshot (148)](https://user-images.githubusercontent.com/73120937/184893216-66e09eff-4ad2-4a16-b8ac-5e75eb159d99.png)

#### ![Screenshot (147)](https://user-images.githubusercontent.com/73120937/184893287-f119f6c6-a74a-42ff-af4d-dc877ddff874.png)

#### ![Screenshot (149)](https://user-images.githubusercontent.com/73120937/184893349-f206cab2-85fb-47d5-b62d-c3ce60daf5bd.png)

#### ![Screenshot (150)](https://user-images.githubusercontent.com/73120937/184893460-05001f31-9252-435f-a06f-7af79ac104c4.png)
