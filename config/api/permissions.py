from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsVendor(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='Vendors').exists():
            return super().has_permission(request, view)
        

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='Customers').exists():
            return super().has_permission(request, view)


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS