from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .serializers import ChatMessageSerializer, UserSerializer
from .models import Message
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from users.models import User
# Create your views here.


class MessageListView(ListAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user1 = int(self.kwargs['user1'])    # the one who sending  the message
        user2 = int(self.kwargs['user2'])    # the one who receives the message 

        queryset = Message.objects.filter(
            Q(sender=user1), Q(receiver=user2), Q(sender_delete=False))
        return queryset


class MessageDelete(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.user:
            requested_user = request.user            # if there is  credentials passing
        else:
            user_id = request.data.get('user_id')    # requested user id  

        message_id = request.data.get('message_id')  # message id 

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
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.user.is_activated:
            requested_user = request.user
        else:
            requested_user = request.data.get('requested_user')    # the one who wanted to clear the history
        second_user = request.data.get('second_user')              # the other user that he's chatting with to be delete the message with

        if requested_user and second_user is None:
            return Response({'error':'requested user id and second user id must be provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            sended_messages = Message.objects.filter(sender_id= requested_user, receiver_id = second_user)
            received_messages = Message.objects.filter(receiver_id=requested_user, sender_id=second_user)
        except Message.DoesNotExist:
            return Response({'error': 'Message not found or user is not the sender or receiver'}, status=status.HTTP_404_NOT_FOUND)
        

        for message in sended_messages:

            print(message)
            message.sender_delete = True
            message.save()

        for message in received_messages:
            message.receiver_delete = True
            message.save()
        return Response({'success':'History cleared successfully'}, status=status.HTTP_200_OK)





class ConnectionList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id=int(self.kwargs['user_id'])
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

