from django.urls import path
from . import views
urlpatterns=[
    path('user-previous-chats/<int:user1>/<int:user2>/',views.MessageListView.as_view()),
    path('delete_message/', views.MessageDelete.as_view()),
    path('delete_message_everyone/', views.MessageDeleteEveryOne.as_view()),
    path('clear_history/', views.CleanHistory.as_view()),

    path('connections/<int:user_id>/', views.ConnectionList.as_view()),   # all the connections
    path('search/', views.ChatSearch.as_view()), 



    path('blocked_users/<int:user_id>/', views.BlockedUsersList.as_view()),
    path('unblock_user/<int:user_id>/<int:blocked_user_id>/', views.UnblockUser.as_view()),

]