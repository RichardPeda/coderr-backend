

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsBusinessUserToCreateOffer(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method == 'POST':
            return bool(request.user and obj.type == 'business')  
        else:
            return False
        
        
class IsOwnerOfOfferOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            print(obj.user)
            print(request.user)
            
            return True
        else:
            print(obj.user)
            print(request.user)

            return bool(request.user == obj.user or request.user.is_superuser)  
        