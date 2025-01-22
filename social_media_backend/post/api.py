from django.http import JsonResponse
from .serializers import PostSerializer
from .models import Post
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .forms import PostForm
from account.models import User
from account.serializers import UserSerializer


@api_view(['GET'])
def post_list(request):
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)
        
    posts = Post.objects.filter(created_by_id__in = list(user_ids))
    serializer = PostSerializer(posts, many=True)

    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def post_list_profile(request, id):
    print(f"Profile endpoint called with id: {id}")
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id) #we can use created_by_id because created_by is foreign key to User 
    posts_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)

    return JsonResponse({
        'posts': posts_serializer.data,
        'user': user_serializer.data
    }, safe=False)

@api_view(['POST'])
def post_create(request):
    form = PostForm(request.data)
    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()
        serializer = PostSerializer(post)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'error add later'})