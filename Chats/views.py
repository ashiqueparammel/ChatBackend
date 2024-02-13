from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .serializers import ChatMessageSerializer
from .models import Message
from django.db.models import Q
# Create your views here.
class MessageListView(ListAPIView):
    serializer_class = ChatMessageSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user1 = int(self.kwargs['user1'])
        user2 = int(self.kwargs['user2'])

        queryset = Message.objects.filter(Q(sender=user1), Q(receiver=user2), Q(sender_delete=False))
        return queryset
