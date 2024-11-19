from rest_framework.permissions import BasePermission, SAFE_METHODS

from userprofile.models import UserProfile


class IsCustomerToPostOrder(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method == 'POST':
            print(obj)
            return bool(request.user and obj.type == 'customer')  
        else:
            return False

class IsBusinessUserOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method == 'DELETE':
            return bool(request.user and request.user.is_staff)
        else:
            try:
                user= UserProfile.objects.get(user=request.user)
                return bool(request.user and obj.business_user == user)
            except:
                return False
        