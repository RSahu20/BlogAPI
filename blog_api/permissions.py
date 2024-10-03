from rest_framework.permissions import BasePermission, SAFE_METHODS

class WriterPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not hasattr(user, 'userprofile'):
            return False
        return user.userprofile.role == 'writer'


class CommentPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not hasattr(user, 'userprofile'):
            return False
        return user.userprofile.role == 'commenter'


class ReadOnlyPermission(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS
