from django.contrib.auth.models import User
from django.http import JsonResponse
from .serializers import BlockedUserSerializer
from .models import BlockedUser
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView,RetrieveUpdateDestroyAPIView
from .serializers import ChatMessageSerializer, UserSerializer
from .models import Message
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from users.models import User
from django.shortcuts import get_object_or_404
from rest_framework.filters import SearchFilter

# Create your views here.


class MessageListView(ListAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]
            
    def get_queryset(self):
        user1 = int(self.kwargs['user1'])    
        user2 = int(self.kwargs['user2'])    
        queryset = Message.objects.filter(
            (Q(sender=user1, receiver=user2) & Q(sender_delete=False)) |
            (Q(sender=user2, receiver=user1) & Q(receiver_delete=False)),  
        )
        return queryset
    


class MessageDelete(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')    
        message_id = request.data.get('message_id')  
        if message_id is None or user_id is None:
            return Response({'error': 'Both message_id and user_id must be provided'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            message = Message.objects.get(id=message_id, sender_id=user_id)
        except Message.DoesNotExist:
            try:
                message = Message.objects.get(
                    id=message_id, receiver_id=user_id)
            except Message.DoesNotExist:
                return Response({'error': 'Message not found or user is not the sender or receiver'}, status=status.HTTP_404_NOT_FOUND)
        if message.sender_delete and message.receiver_delete:
            return Response({'error': 'Message already marked as deleted'}, status=status.HTTP_400_BAD_REQUEST)
        if message.sender_id == user_id:
            message.sender_delete = True
        elif message.receiver_id == user_id:
            message.receiver_delete = True
        message.save()

        return Response({'success': 'Message marked as deleted'}, status=status.HTTP_200_OK)


class CleanHistory(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        requested_user = request.data.get('requested_user')
        second_user = request.data.get('second_user')
        if requested_user and second_user is None:
            return Response({'error': 'requested user id and second user id must be provided'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            sended_messages = Message.objects.filter(
                sender_id=requested_user, receiver_id=second_user)
            received_messages = Message.objects.filter(
                receiver_id=requested_user, sender_id=second_user)
        except Message.DoesNotExist:
            return Response({'error': 'Message not found or user is not the sender or receiver'}, status=status.HTTP_404_NOT_FOUND)
        for message in sended_messages:
            print(message)
            message.sender_delete = True
            message.save()

        for message in received_messages:
            message.receiver_delete = True
            message.save()
        return Response({'success': 'History cleared successfully'}, status=status.HTTP_200_OK)
    



class ConnectionList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_id = int(self.kwargs['user_id'])
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BlockedUsersList(APIView):
    def get(self, request, user_id, *args, **kwargs):
        blocked_users = BlockedUser.objects.filter(user_id=user_id)
        
        if blocked_users.exists():
            serializer = BlockedUserSerializer(blocked_users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'message': 'No blocked users found for the given user id.'}, status=status.HTTP_404_NOT_FOUND)
    def post(self, request, *args, **kwargs):
        serializer = BlockedUserSerializer(data=request.data)
        if serializer.is_valid():
            blocked_user = 0
            for i, value in enumerate(request.data.get('blocked_users', [])):
                blocked_user = value
            if blocked_user:
                check = BlockedUser.objects.filter(user=request.data.get('user'), blocked_users=blocked_user).exists()
                if check:
                    return Response({'error':'User is already blocked'}, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.exceptions import ValidationError


class ChatSearch(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.filter(is_superuser=False, is_active=True)
    filter_backends = [SearchFilter]
    search_fields = ["username", "email",'phone_number']
    serializer_class = UserSerializer

class UnblockUser(APIView):
    def post(self, request, *args, **kwargs):
        try:
            user_id = int(kwargs['user_id'])
            blocked_user_id = int(kwargs['blocked_user_id'])
        except ValueError:
            return Response({'error': 'Invalid user ID or blocked user ID'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            blocked_user = BlockedUser.objects.get(user_id=user_id, blocked_users__id=blocked_user_id)
        except BlockedUser.DoesNotExist:
            return Response({'error': 'Blocked user not found'}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            user_to_unblock = User.objects.get(id=blocked_user_id)
        except User.DoesNotExist:
            return Response({'error': 'User to unblock not found'}, status=status.HTTP_404_NOT_FOUND)

        blocked_user.unblock_user(user_to_unblock)
        return Response({'success': 'Unblocked successfully'}, status=status.HTTP_200_OK)
    
    
class MessageDeleteEveryOne(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user_id = request.data.get('user_id')    
        message_id = request.data.get('message_id')  
        if message_id is None or user_id is None:
            return Response({'error': 'Both message_id and user_id must be provided'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            message = Message.objects.get(id=message_id, sender_id=user_id)
        except Message.DoesNotExist:
            try:
                message = Message.objects.get(
                    id=message_id, receiver_id=user_id)
            except Message.DoesNotExist:
                return Response({'error': 'Message not found or user is not the sender or receiver'}, status=status.HTTP_404_NOT_FOUND)
        if message.sender_delete and message.receiver_delete:
            return Response({'error': 'Message already marked as deleted'}, status=status.HTTP_400_BAD_REQUEST)
        if message.sender_id == user_id:
            message.sender_delete = True
            message.receiver_delete = True
            
        elif message.receiver_id == user_id:
            message.sender_delete = True
            message.receiver_delete = True
        message.save()

        return Response({'success': 'Message marked as deleted'}, status=status.HTTP_200_OK)
     


