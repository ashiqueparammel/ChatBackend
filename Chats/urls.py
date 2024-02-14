from django.urls import path
from . import views
urlpatterns=[
    path('user-previous-chats/<int:user1>/<int:user2>/',views.MessageListView.as_view()),
    path('delete_message/', views.MessageDelete.as_view()),
    path('clear_history/', views.CleanHistory.as_view()),

    path('connections/<int:user_id>/', views.ConnectionList.as_view()),
]