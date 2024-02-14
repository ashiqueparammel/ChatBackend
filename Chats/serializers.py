from rest_framework import serializers
from .models import Message


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        # fields = ['message', 'sender_email']
        fields = '__all__'


