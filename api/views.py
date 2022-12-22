from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters

from .models import Post, Comment, Follow
from .serializers import PostSerializer, CommentSerializer, FollowSerizalizer
from .permissions import IsOwnerOrReadOnly

User = get_user_model()

class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsOwnerOrReadOnly,)

    def get_queryset(self):
        queryset = Comment.objects.filter(post=self.kwargs['post_id'])
        return queryset

    def perform_create(self, serializer):
        post = get_object_or_404(Post, id = self.kwargs['post_id'])
        serializer.save(author = self.request.user, post=post)

class FollowViewSet(ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerizalizer
    permission_classes = (IsOwnerOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=user__username','=following__username')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
