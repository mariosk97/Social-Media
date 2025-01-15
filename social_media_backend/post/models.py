from django.db import models
import uuid
from account.models import User
from django.utils.timesince import timesince

class PostAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='post_attachments')
    created_by = models.ForeignKey(User, related_name='post_attachments', on_delete=models.CASCADE)


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)

    attachments = models.ManyToManyField(PostAttachment, blank=True)

    class Meta:
        ordering = ('-created_at',)

    def created_at_formatted (self):
        return timesince(self.created_at)    
