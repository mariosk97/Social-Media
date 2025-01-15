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
    friendship_request = FriendshipRequest.objects.create(created_for=user, created_by=request.user)

    return JsonResponse({'message': 'friend request created'})

@api_view(['GET'])
def friends(request, pk):
    requests_data = []
    user = User.objects.get(pk=pk)

    if user == request.user:
        requests = FriendshipRequest.objects.filter(created_for=request.user)
        requests_serializer  = FriendshipRequestSerializer(requests, many=True)
        requests_data  = requests_serializer.data

    friends = user.friends.all()

    return JsonResponse({
        'user': UserSerializer(user).data,
        'friends': UserSerializer(friends, many=True).data,
        'requests': requests_data
    }, safe=False)


        
