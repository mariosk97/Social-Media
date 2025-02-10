from rest_framework import serializers
from account.serializers import UserSerializer
from .models import Conversation, ConversationMessage

class ConversationSerializer(serializers.ModelSerializer):
    users = UserSerializer(read_only=True, many=True) 

    class Meta:
        model = Conversation
        fields = ('id', 'users', 'modified_at_formatted')

class ConversationMessageSerializer(serializers.ModelSerializer):
    sent_to = UserSerializer(read_only=True) 
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = ConversationMessage
        fields = ('id', 'sent_to', 'body', 'created_at_formatted', 'created_by')

class ConversationDetailSerializer(serializers.ModelSerializer):
    messages = ConversationMessageSerializer(read_only=True, many=True)

    class Meta:    
        model = Conversation
        fields = ('id', 'users', 'modified_at_formatted', 'messages')
