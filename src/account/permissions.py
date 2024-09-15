from rest_framework import permissions

from account.models import Account


class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = Account.objects.get(username=request.query_params["username"])
        except:
            return False

        if request.user.is_superuser:
            return True

        if not request.user == user:
            return False
        else:
            return True


class IsBusiness(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user = request.user
        except:
            return False

        # if user.is_superuser:
        #     return True

        if not user.is_Business:
            return False
        else:
            return True
