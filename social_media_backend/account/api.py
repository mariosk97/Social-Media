from django.http import JsonResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import SignUpForm
from .models import User, FriendshipRequest
from .serializers import UserSerializer, FriendshipRequestSerializer

@api_view(['GET'])
def me(request):
    return JsonResponse({
        'id': request.user.id,
        'email': request.user.email,
        'name': request.user.name,
    })
    
@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'

    form = SignUpForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })

    if form.is_valid():
        form.save()
    else:
        message = 'error'
        print(form.errors) 

    return JsonResponse({'message': message})

@api_view(['POST'])
def send_friendship_request(request, pk):
    user = User.objects.get(pk=pk)
    is_request_sent1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    is_request_sent2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)

    if not is_request_sent1 or not is_request_sent2:
        FriendshipRequest.objects.create(created_for=user, created_by=request.user)

        return JsonResponse({'message': 'friend request created'})
    else:
        return JsonResponse({'message': 'request already sent'})

@api_view(['GET'])
def friends(request, pk):
    requests_data = []
    user = User.objects.get(pk=pk)

    if user == request.user:
        requests = FriendshipRequest.objects.filter(created_for=request.user, status=FriendshipRequest.SENT)
        requests_serializer  = FriendshipRequestSerializer(requests, many=True)
        requests_data  = requests_serializer.data

    friends = user.friends.all()

    return JsonResponse({
        'user': UserSerializer(user).data,
        'friends': UserSerializer(friends, many=True).data,
        'requests': requests_data
    }, safe=False)

@api_view(['POST'])
def handle_request(request, pk, status):
    user = User.objects.get(pk=pk) #user that made the friend request
    friendship_request = FriendshipRequest.objects.filter(created_for=request.user).get(created_by=user)
    friendship_request.status = status
    friendship_request.save()

    user.friends.add(request.user)
    user.friends_count = user.friends_count + 1
    user.save()

    request_user = request.user
    request_user.friends_count = request_user.friends_count + 1
    request_user.save()
        
    return JsonResponse({'message': 'friend request updated'})