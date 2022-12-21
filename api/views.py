from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet

from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsOwnerOrReadOnly

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