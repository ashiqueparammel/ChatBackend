# from django.contrib.auth.models import User
from .models import BlockedUser,Message
from users.models import User 

from rest_framework import serializers
from .models import Message


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        # fields = ['message', 'sender_email']
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    connections = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'profile_image', 'profile_cover_image',
                  'phone_number', 'is_google', 'connections')

    def get_connections(self, user):
        sent_messages = Message.objects.filter(sender=user)
        received_messages = Message.objects.filter(receiver=user)
        connections = set()

        for message in sent_messages:
            connections.add(message.receiver_id)

        for message in received_messages:
            connections.add(message.sender_id)

        blocked_users = BlockedUser.objects.filter(user=user)
        blocked_user_ids = blocked_users.values_list('blocked_users', flat=True)

        connected_user_ids = set(connections) - set(blocked_user_ids)
        connected_users = User.objects.filter(id__in=connected_user_ids)

        return connected_users.values('id', 'username', 'email', 'profile_image', 'profile_cover_image', 'phone_number', 'is_google')



class BlockedUserSerializer(serializers.ModelSerializer):
    blocked_users = serializers.PrimaryKeyRelatedField(
        many=True, queryset=User.objects.all())

    class Meta:
        model = BlockedUser
        fields = ['user', 'blocked_users']

    def create(self, validated_data):
        blocked_users_data = validated_data.pop('blocked_users')
        blocked_user = BlockedUser.objects.create(**validated_data)
        for user_data in blocked_users_data:
            blocked_user.blocked_users.add(user_data)
        return blocked_user
