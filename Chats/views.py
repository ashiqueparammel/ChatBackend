from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .serializers import ChatMessageSerializer
from .models import Message
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
# Create your views here.


class MessageListView(ListAPIView):
    serializer_class = ChatMessageSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user1 = int(self.kwargs['user1'])
        user2 = int(self.kwargs['user2'])

        queryset = Message.objects.filter(
            Q(sender=user1), Q(receiver=user2), Q(sender_delete=False))
        return queryset


class MessageDelete(APIView):
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data  # Assuming data is passed in the request body

        message_id = data.get('message_id')
        user_id = data.get('user_id')

        if message_id is None or user_id is None:
            return Response({'error': 'Both message_id and user_id must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Check if the user is the sender
            message = Message.objects.get(id=message_id, sender_id=user_id)
        except Message.DoesNotExist:
            try:
                # Check if the user is the receiver
                message = Message.objects.get(
                    id=message_id, receiver_id=user_id)
            except Message.DoesNotExist:
                return Response({'error': 'Message not found or user is not the sender or receiver'}, status=status.HTTP_404_NOT_FOUND)

        # Check if the message is already marked as deleted
        if message.sender_delete and message.receiver_delete:
            return Response({'error': 'Message already marked as deleted'}, status=status.HTTP_400_BAD_REQUEST)

        # Mark the message as deleted
        if message.sender_id == user_id:
            message.sender_delete = True
        elif message.receiver_id == user_id:
            message.receiver_delete = True
        message.save()

        return Response({'success': 'Message marked as deleted'}, status=status.HTTP_200_OK)


class CleanHistory(APIView):
    def post(self, request, *args, **kwargs):
        
