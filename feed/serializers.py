from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Feed, Hashtag, Mention, FeedComment

class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ('id', 'name')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class MentionSerializer(serializers.ModelSerializer):
    mentioned_by = UserSerializer()
    mentioned_user = UserSerializer()

    class Meta:
        model = Mention
        fields = ('id', 'mentioned_by', 'mentioned_user')

class FeedCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = FeedComment
        fields = ('id', 'user', 'content', 'created_at', 'updated_at')

class FeedDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    hashtags = HashtagSerializer(many=True)
    mentions = MentionSerializer(many=True)
    comments = FeedCommentSerializer(many=True)

    class Meta:
        model = Feed
        fields = ('id', 'user', 'title', 'content', 'likes', 'hashtags', 'created_at', 'updated_at', 'mentions', 'comments')

class FeedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ('id', 'user', 'title', 'content', 'likes', 'hashtags', 'created_at', 'updated_at', 'mentions', 'comments')