from django.contrib import admin
from . models import FriendshipRequest, User

admin.site.register(User)
admin.site.register(FriendshipRequest)
