from django.db import models
from django.contrib.auth.models import User


class Hashtag(models.Model):
    name = models.CharField(max_length=255)

class Feed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(null=True, blank=True)
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name="liked_feeds", blank=True)
    hashtags = models.ManyToManyField(Hashtag, related_name="feeds_hashtag", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

class Media(models.Model):
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE, related_name='feed_media')
    file = models.FileField(upload_to='media/')
    is_image = models.BooleanField(default=True)

    def __str__(self):
        return self.file.name
    
    
class FeedComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_comment=models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE , related_name='replies')    


