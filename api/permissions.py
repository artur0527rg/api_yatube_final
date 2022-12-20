from rest_framework.permissions import IsAuthenticatedOrReadOnly, SAFE_METHODS

class IsOwnerOrReadOnly(IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            if request.user == obj.author:
                return True
            return False
        return True
            
        