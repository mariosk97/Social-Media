from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse

from account.models import User
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

@api_view(['POST'])
def conversation_send_message(request, pk):
    conversation = Conversation.objects.filter(users__in = list([request.user])).get(pk=pk)

    for user in conversation.users.all():
        if user != request.user:
            sent_to = user

    conversation_message = ConversationMessage.objects.create(
        conversation = conversation,
        body = request.data.get('body'),
        created_by = request.user,
        sent_to = sent_to
    )

    serializer = ConversationMessageSerializer(conversation_message)

    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def conversation_get_or_create(request, user_pk):
    user = User.objects.get(pk=user_pk)    
    conversations = Conversation.objects.filter(users__in = list([request.user])).filter(users__in=list([user])) #first get all the conversations of request user then check if that user alread has a conversation pk user
    if conversations.exists():
        conversation = conversations.first()
    else:
        conversation = Conversation.objects.create()
        conversation.users.add(request.user, user)
        conversation.save()

    serializer = ConversationDetailSerializer(conversation)    

    return JsonResponse(serializer.data, safe=False)        