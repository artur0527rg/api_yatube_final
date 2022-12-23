from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

from .models import Post, Comment, Follow, Group


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ('id', 'author', 'post', 'text', 'created')
        model = Comment
        read_only_fields = ('post',)

class FollowSerizalizer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username",
        # queryset=User.objects.all(),
        read_only=True
        )
    following = serializers.SlugRelatedField(
        slug_field = 'username',
        queryset=User.objects.all()
        )

    def validate(self, attrs):
        if self.context['request'].user == attrs['following']:
            raise serializers.ValidationError('Вы не можете подписаться сами на себя', code=400)
        if Follow.objects.filter(
            user = self.context['request'].user,
            following = attrs['following']
            ).exists():
            raise serializers.ValidationError('Вы не можете подписатся на пользователся два раза')
        return attrs

    class Meta():
        model = Follow
        fields = ("user","following")

class GroupSerializer(serializers.ModelSerializer):

    class Meta():
        model = Group
        fields = ('id', 'title')