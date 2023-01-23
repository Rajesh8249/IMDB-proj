from rest_framework import permissions

class IsAdminOrReadOnly(permissions. IsAdminUser):
    def has_permission(self, request, view):
        # admin_permissions = bool(request.user and request.user.is_staff)
        # return  request.method == "GET" or admin_permissions
        
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return  bool(request.user and request.user.is_staff)



class IsReviewUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.review_user == request.user or request.user.is_staff
