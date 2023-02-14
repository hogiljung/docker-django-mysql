from rest_framework import serializers
from .models import Post, Content
from sign.models import Users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('id', 'username')

class ContentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = ('post_id', 'content')
        read_only_fields = ()

class PostSerializer(serializers.ModelSerializer):
    #post = ContentsSerializer(many=True, read_only=True)
    user = UserSerializer(many=True, read_only=True)
    class Meta:
        model = Post
        fields = ('id', 'title', 'brief_description', 'created_date', 'updated_date', 'user')
        read_only_fields = ()

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = UserSerializer(instance.user_id).data
        return response
