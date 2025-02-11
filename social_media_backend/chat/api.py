from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse
from .serializers import ConversationSerializer, ConversationMessageSerializer, ConversationDetailSerializer
from .models import Conversation, ConversationMessage

@api_view(['GET'])
def conversation_list(request):
    conversations = Conversation.objects.filter(users__in = list([request.user]))

    print(conversations)

    return JsonResponse({'aas': 'tss'})
