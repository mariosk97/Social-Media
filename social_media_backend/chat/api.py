from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse
from .serializers import ConversationSerializer, ConversationMessageSerializer, ConversationDetailSerializer
from .models import Conversation, ConversationMessage

@api_view(['GET'])
def conversation_list(request):
    conversations = Conversation.objects.filter(users__in = list([request.user]))
    serializer = ConversationSerializer(conversations, many=True)

    print(conversations)

    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def conversation_detail(request, pk):
    conversation = Conversation.objects.filter(users__in = list([request.user])).get(pk=pk) #first make sure user is a member of the conversation, then get the conversation
    serializer = ConversationDetailSerializer(conversation)

    return JsonResponse(serializer.data, safe=False)