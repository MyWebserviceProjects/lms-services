from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user
class IsOwnerOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):      
        return obj.owner == request.user
    
class IsAdminOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):        
        return request.user.groups.filter(name='admin').exists()
    
class IsAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.groups.filter(name='admin').exists()
    
class IsFacultyOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):        
        return request.user.groups.filter(name='faculty').exists()

class IsFacultyAdminOrReadOnly(permissions.BasePermission):
        
    def has_object_permission(self, request, view, obj):
       
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.groups.filter(name='faculty').exists() or request.user.groups.filter(name='admin').exists():
            return True
        else:
            return False
    
class IsFacultyOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return  request.user.groups.filter(name='faculty').exists()

class IsStudentOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):        
        return request.user.groups.filter(name='student').exists()

class IsStudentOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.groups.filter(name='student').exists()
