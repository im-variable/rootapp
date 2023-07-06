from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Feed, Hashtag, FeedComment

class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ('id', 'name')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')

class FeedCommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = FeedComment
        fields = ('id', 'user', 'content', 'created_at', 'updated_at')

class FeedDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    hashtags = HashtagSerializer(many=True)
    comments = FeedCommentSerializer(many=True, source='feedcomment_set')

    class Meta:
        model = Feed
        fields = ('id', 'user', 'title', 'content', 'likes', 'hashtags', 'created_at', 'updated_at', 'comments')

# for post method
class FeedSerializer(serializers.ModelSerializer):
    hashtags = HashtagSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = Feed
        fields = ('id', 'user', 'title', 'content', 'hashtags', 'created_at', 'updated_at')

    def to_internal_value(self, data):    
        hashtags_data = data.get('hashtags', [])
        data['hashtags'] = [{'name': name.lower()} for name in hashtags_data]
        
        data['user'] = self.context.get('user')
        
        return super().to_internal_value(data)

    def create(self, validated_data):
        hashtags_data = validated_data.pop('hashtags', [])
        feed = Feed.objects.create(**validated_data)
        for hashtag_data in hashtags_data:
            hashtag_name = hashtag_data.get('name')
            if hashtag_name:
                hashtag, _ = Hashtag.objects.get_or_create(name=hashtag_name.lower())
                feed.hashtags.add(hashtag)        
        return feed

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.save()
        hashtags_data = validated_data.get('hashtags', [])
        self._process_hashtags(instance, hashtags_data)
        return instance 
       
    def _process_hashtags(self, feed, hashtags_data):
        existing_hashs = feed.hashtags.all()
        hash_to_remove = [hashtag for hashtag in existing_hashs if hashtag.name not in [data.get('name').lower() for data in hashtags_data]]
        feed.hashtags.remove(*hash_to_remove)

        instance_hashs = [hashtag.name.lower() for hashtag in existing_hashs]
        
        for hashtag_data in hashtags_data:
            hashtag_name = hashtag_data.get('name')
            if hashtag_name and hashtag_name.lower() not in instance_hashs:
                hashtag, _ = Hashtag.objects.get_or_create(name=hashtag_name.lower())
                feed.hashtags.add(hashtag)
                
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        hashtags = instance.hashtags.values_list('name', flat=True)
        representation['hashtags'] = list(hashtags)
        return representation
    