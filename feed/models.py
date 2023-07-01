from django.db import models
from django.contrib.auth.models import User


class Hashtag(models.Model):
    name = models.CharField(max_length=255)

class Feed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(null=True, blank=True)
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name="liked_feeds")
    hashtags = models.ManyToManyField(Hashtag, related_name="feeds_hashtag")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

class Mention(models.Model):
    mentioned_by = models.ForeignKey(User, on_delete=models.CASCADE)
    mentioned_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentions')
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)

class FeedComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    parent_comment=models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE , related_name='replies')    


