from .models import User, Message
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

        connected_users = User.objects.filter(
            id__in=connections).exclude(id=user.id)
        return connected_users.values('id', 'username', 'email', 'profile_image', 'profile_cover_image', 'phone_number', 'is_google' )
