from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCustomerToPostOrder(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method == 'POST':
            print(obj)
            return bool(request.user and obj.type == 'customer')  
        else:
            return False