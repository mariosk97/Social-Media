import django
import os
import sys

from datetime import timedelta
from collections import Counter
from django.utils import timezone

sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "social_media_backend.settings")
django.setup()

from post.models import Post, Trend

def extract_hashtags(text, trends):
    for word in text.split():
        if word[0] == '#':
            trends.append(word[1:])

    return trends        

posts = Post.objects.all()
trends = []

for post in posts:
    extract_hashtags(post.body, trends)

trends_counter = Counter(trends)

for trend in trends_counter:
    print(trend)
