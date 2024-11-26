from rest_framework.permissions import BasePermission, SAFE_METHODS
from userprofile.models import UserProfile

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
            return True
        else:
            user = UserProfile.objects.get(user=request.user)
            return bool(obj.user == user or request.user.is_superuser)  
        