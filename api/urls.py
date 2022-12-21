from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'posts/(?P<post_id>[0-9]+)/comments', CommentViewSet)

urlpatterns = [
    path('', include(router.urls))
]
