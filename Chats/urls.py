from django.urls import path
from . import views
urlpatterns=[
    path('user-previous-chats/<int:user1>/<int:user2>/',views.MessageListView.as_view())
]