import django
import os
import sys

from datetime import timedelta
from collections import Counter
from django.utils import timezone

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_media_backend.settings")
django.setup()

from post.models import Post

posts = Post.objects.all()
print(posts)

trends = []